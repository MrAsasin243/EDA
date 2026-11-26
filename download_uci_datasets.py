#!/usr/bin/env python3
"""Download curated UCI datasets for the EDA course using the official UCI API.

Examples:
  python download_uci_datasets.py --list
  python download_uci_datasets.py --only online_retail,bike_sharing
  python download_uci_datasets.py                 # download all 12 datasets
  python download_uci_datasets.py --only 352 --force

The script downloads only after explicit user invocation. Data are stored under data/raw/;
metadata and the original source attribution are stored under data/metadata/.
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
from datetime import datetime, timezone

DATASETS = [
 (275,'bike_sharing','Bike Sharing','10.24432/C5W894','https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset','Fanaee-T, H. (2013). Bike Sharing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894.'),
 (352,'online_retail','Online Retail','10.24432/C5BW33','https://archive.ics.uci.edu/dataset/352/online+retail','Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33.'),
 (222,'bank_marketing','Bank Marketing','10.24432/C5K306','https://archive.ics.uci.edu/dataset/222/bank+marketing','Moro, S., Rita, P., & Cortez, P. (2014). Bank Marketing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306.'),
 (2,'adult','Adult (Census Income)','10.24432/C5XW20','https://archive.ics.uci.edu/dataset/2/adult','Becker, B., & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20.'),
 (186,'wine_quality','Wine Quality','10.24432/C56S3T','https://archive.ics.uci.edu/dataset/186/wine+quality','Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Wine Quality [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T.'),
 (320,'student_performance','Student Performance','10.24432/C5TG7T','https://archive.ics.uci.edu/dataset/320/student+performance','Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T.'),
 (374,'appliances_energy','Appliances Energy Prediction','10.24432/C5VC8G','https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction','Candanedo, L. (2017). Appliances Energy Prediction [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5VC8G.'),
 (360,'air_quality','Air Quality','10.24432/C59K5F','https://archive.ics.uci.edu/dataset/360/air+quality','Vito, S. (2008). Air Quality [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C59K5F.'),
 (468,'online_shoppers','Online Shoppers Purchasing Intention','10.24432/C5F88Q','https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset','Sakar, C., & Kastro, Y. (2018). Online Shoppers Purchasing Intention Dataset [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5F88Q.'),
 (350,'default_credit_card','Default of Credit Card Clients','10.24432/C55S3H','https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients','Yeh, I. (2009). Default of Credit Card Clients [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H.'),
 (292,'wholesale_customers','Wholesale Customers','10.24432/C5030X','https://archive.ics.uci.edu/dataset/292/wholesale+customers','Cardoso, M. (2013). Wholesale customers [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5030X.'),
 (1,'abalone','Abalone','10.24432/C55C7W','https://archive.ics.uci.edu/dataset/1/abalone','Nash, W., Sellers, T., Talbot, S., Cawthorn, J., & Ford, W. (1994). Abalone [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55C7W.'),
]

def main():
    parser=argparse.ArgumentParser(description='Download real datasets from the UCI Machine Learning Repository.')
    parser.add_argument('--only', help='Comma-separated dataset slugs or UCI IDs; default: all')
    parser.add_argument('--list', action='store_true', help='List available datasets and exit')
    parser.add_argument('--force', action='store_true', help='Replace existing CSV files')
    parser.add_argument('--output-dir', default='data', help='Output directory (default: ./data)')
    args=parser.parse_args()
    if args.list:
        for did,slug,name,*_ in DATASETS: print(f'{slug:24} UCI {did:>3}  {name}')
        return 0
    selected=DATASETS
    if args.only:
        tokens={x.strip().lower() for x in args.only.split(',') if x.strip()}
        selected=[d for d in DATASETS if d[1].lower() in tokens or str(d[0]) in tokens]
        unknown=tokens-{d[1].lower() for d in selected}-{str(d[0]) for d in selected}
        if unknown: parser.error('Unknown dataset(s): '+', '.join(sorted(unknown)))
    try:
        import pandas as pd
        from ucimlrepo import fetch_ucirepo
    except ImportError as exc:
        print('Missing dependency. Install with: pip install -r requirements-eda-real.txt',file=sys.stderr)
        return 2
    root=Path(args.output_dir); raw=root/'raw'; meta_dir=root/'metadata'
    raw.mkdir(parents=True,exist_ok=True); meta_dir.mkdir(parents=True,exist_ok=True)
    failures=[]
    for did,slug,name,doi,url,citation in selected:
        csv_path=raw/f'{slug}.csv'; meta_path=meta_dir/f'{slug}.json'
        if csv_path.exists() and not args.force:
            print(f'[SKIP] {name}: {csv_path} already exists (use --force to replace)'); continue
        print(f'[FETCH] {name} (UCI id={did}) ...',flush=True)
        try:
            obj=None; last_exc=None
            for attempt in range(3):
                try:
                    obj=fetch_ucirepo(id=did)
                    break
                except Exception as exc:
                    last_exc=exc
                    if attempt<2: time.sleep(2*(attempt+1))
            if obj is None: raise RuntimeError(f'UCI API failed after retries: {last_exc}')
            data=obj.data
            features=getattr(data,'features',None)
            targets=getattr(data,'targets',None)
            original=getattr(data,'original',None)
            if isinstance(original,pd.DataFrame) and not original.empty:
                frame=original.copy()
            else:
                parts=[]
                if isinstance(features,pd.DataFrame) and not features.empty: parts.append(features.copy())
                if isinstance(targets,pd.DataFrame) and not targets.empty: parts.append(targets.copy())
                if not parts: raise ValueError('UCI API returned no usable DataFrame in features, targets or original.')
                frame=pd.concat(parts,axis=1)
            # Keep all fields, but guarantee unique column labels for CSV round-tripping.
            seen={}; columns=[]
            for col in map(str,frame.columns):
                n=seen.get(col,0); seen[col]=n+1
                columns.append(col if n==0 else f'{col}__{n+1}')
            frame.columns=columns
            frame.to_csv(csv_path,index=False,encoding='utf-8')
            variables=getattr(obj,'variables',None)
            variable_records=[]
            if isinstance(variables,pd.DataFrame): variable_records=variables.where(pd.notna(variables),None).to_dict(orient='records')
            metadata={
                'name':name,'uci_id':did,'repository':'UCI Machine Learning Repository',
                'official_url':url,'doi':doi,'citation':citation,'license':'CC BY 4.0 (as stated on the UCI dataset page)',
                'downloaded_at_utc':datetime.now(timezone.utc).isoformat(),
                'rows':int(len(frame)),'columns':list(map(str,frame.columns)),
                'variables':variable_records,
                'data_file':str(csv_path.as_posix()),
                'note':'UCI API materialization. Consult the official page for dataset documentation, caveats and citation.'
            }
            meta_path.write_text(json.dumps(metadata,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
            print(f'[OK] {name}: {len(frame):,} rows × {len(frame.columns)} columns -> {csv_path}',flush=True)
        except Exception as exc:
            failures.append((name,str(exc)))
            print(f'[FAIL] {name}: {exc}',file=sys.stderr,flush=True)
    if failures:
        print('\nSome downloads failed:',file=sys.stderr)
        for name,err in failures: print(f' - {name}: {err}',file=sys.stderr)
        return 1
    print('\nDone. Keep the data/raw and data/metadata folders together with the notebooks.')
    return 0

if __name__=='__main__': raise SystemExit(main())
