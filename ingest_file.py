from datetime import datetime
import re

from collections import defaultdict

from models import DBEngine, Log


def read_log_line():
    with open('latest.log') as logfile:
        yield from logfile

def main():
    skipped_log_lines = []
    line_count = 0
    logid_counter = defaultdict(int)
    session = None
    session = DBEngine().get_session()

    for line in read_log_line():
        try:
            #Parse
            log_entry = line.replace('\n','').split('\\t')

            #Validate:
            if log_entry[1] not in ['INFO','WARNING','ERROR','INFO','DEBUG']:
                skipped_log_lines.append(line)
                continue

            #Generate log id
            base_id = re.sub(r'[:\- ]', '', log_entry[0])
            log_id = base_id+'-'+str(logid_counter[base_id])
            logid_counter[base_id]+=1

            #Insert into db
            date_object = datetime.strptime(log_entry[0], "%Y-%m-%d %H:%M:%S")
            new_log = Log(
                id=log_id,
                time=date_object,
                level=log_entry[1],
                component=log_entry[2],
                message=log_entry[3]
            )
            session.add(new_log)
            session.commit()
            line_count+=1
        except Exception as e:
            print(f"Error in parsing/inserting log line - {log_entry}\nError message:",str(e))
            continue
        finally:
            if session:
                session.close()

    print("Data ingestion completed succesfully!")
    print(f"Inserted {line_count} lines")
    print(f"Skipped {len(skipped_log_lines)} lines")

main()

#TODO : Set this file in cron schedule daily/weekly/other interval to ingest latest logs. 
#As of now fetches file from the same directory but can be configured to pick file from any desired source.