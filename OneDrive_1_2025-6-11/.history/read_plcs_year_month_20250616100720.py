import glob
import os
import pandas as pd

def read_plcs_year_month(path2project, year_month):
    plcs_in_year_month = glob.glob(os.path.join(path2project, 'data', year_month, '*_*.plc'))
    dfs = []
    
    for filename in plcs_in_year_month:
        # Try different encodings
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        rows = None
        
        for encoding in encodings:
            try:
                with open(filename, encoding=encoding) as f:
                    rows = [line.replace('\n', '').split(';') for line in f]
                break  # If successful, break the encoding loop
            except UnicodeDecodeError:
                continue
        
        if rows is None:
            print(f"Warning: Could not read file {filename} with any of the attempted encodings")
            continue
            
        if rows:
            df = pd.DataFrame(rows[1:], columns=rows[0])
            dfs.append(df)
    
    if not dfs:
        return pd.DataFrame()  # Return empty DataFrame if no files could be read
        
    return pd.concat(dfs, ignore_index=True) 