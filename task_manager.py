import time
import os
from datetime import datetime
import psutil
import pandas as pd

def proc_information():
  
    procs = []
    for proc in psutil.process_iter():
     
        with proc.oneshot():
      
            proc_identity = proc.pid
            if proc_identity == 0:
               
                continue
           
            name = proc.name()
            try:
                name_of_user = proc.username()
            except psutil.AccessDenied:
                name_of_user = "N/A"
            try:
               time_of_creation = datetime.fromtimestamp(proc.create_time())
            except OSError:
              
               time_of_creation = datetime.fromtimestamp(psutil.boot_time())
            try:
               
                memory_required = proc.memory_full_info().uss
            except psutil.AccessDenied:
                memory_required = 0
           
            io_counters = proc.io_counters()
            read_bytes_required = io_counters.read_bytes
            write_bytes_required = io_counters.write_bytes
           
            total_threads = proc.num_threads()
            
            try:
                
                nice_format = int(proc.nice())
            except psutil.AccessDenied:
                nice_format = 0
            try:
              
                crs = len(proc.cpu_affinity())
            except psutil.AccessDenied:
                crs = 0
            
            sys_percent= proc.cpu_percent()
            
            currstatus = proc.status()
            
           
           
            
        procs.append({
            'process identity': proc_identity, 'name': name, 'creation_time':time_of_creation,
            'cores': crs, 'cpu_required': sys_percent, 'status': currstatus, 'nice': nice_format,
            'memory_required': memory_required, 'read_bytes_required': read_bytes_required, 'write_bytes_required': write_bytes_required,
            'total_threads': total_threads, 'username': name_of_user,
        })

    return procs
def size(bytes):
 
    for unit in ['', 'L', 'Q', 'A', 'G', 'U']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def construct_dataframe(procs):
   
    df = pd.DataFrame(procs)
    
    df.set_index('process identity', inplace=True)
   
    df.sort_values(sort_by, inplace=True, ascending=not descending)
   
    df['memory_required'] = df['memory_required'].apply(size)
    df['write_bytes_required'] = df['write_bytes_required'].apply(size)
    df['read_bytes_required'] = df['read_bytes_required'].apply(size)
   
    df['creation_time'] = df['creation_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
   
    df = df[clmns.split(",")]
    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="proc Viewer & Monitor")
    parser.add_argument("-c", "--columns", help="""what are the columns to show.
                                                
                                                Default is name,cpu_required,memory_required,read_bytes_required,write_bytes_required,status,creation_time,nice,total_threads,cores.""",
                        default="name,cpu_required,memory_required,read_bytes_required,write_bytes_required,status,creation_time,nice,total_threads,cores")
    parser.add_argument("-s", "--sort-by", dest="sort_by", help="Decides from which column shold sorting start.", default="memory_required")
    parser.add_argument("--descending", action="store_true", help="Decides in which order to sort.")
    parser.add_argument("-d", help="finds total number of processes,all if 0 is given, default is 20 .", default=20)
    parser.add_argument("-u", "--live_updates_are", action="store_true", help="Decides whether to give live updates")

   
    args = parser.parse_args()
    clmns = args.columns
    sort_by = args.sort_by
    descending = args.descending
    x = int(args.d)
    live_update = args.live_updates_are
   
    procs = proc_information()
    df = construct_dataframe(procs)
    if x == 0:
        print(df.to_string())
    elif x > 0:
        print(df.head(x).to_string())
   
    while live_update:
       
        procs = proc_information()
        df = construct_dataframe(procs)
        #
        os.system("cls") if "nt" in os.name else os.system("clear")
        if x == 0:
            print(df.to_string())
        elif x > 0:
            print(df.head(x).to_string())
        time.sleep(5)
