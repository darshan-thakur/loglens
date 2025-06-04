from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from datetime import datetime
import re

from models import DBEngine, Log

app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(status_code=302, url=f"/logs/")
    
@app.get("/logs/")
def get_logs(level: str = None, component : str = None, start_time: str = None, end_time: str = None, page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    start_time_object = end_time_object = None
    session = None
    try:
        session = DBEngine().get_session()
        filters = []
        if level:
            if level not in ['INFO','WARNING','ERROR','INFO','DEBUG']:
                raise ValueError
            filters.append(Log.level == level) #NOTE for me: The expression resolves to a BinaryExpression object that can still be used as a valid filter
        if component:
            filters.append(Log.component == component)
        if start_time:
            start_time_object = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
            filters.append(Log.time >= start_time_object)
        if end_time:
            end_time_object = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
            filters.append(Log.time < end_time_object)
        if (start_time_object and end_time_object) and start_time_object > end_time_object:
            raise ValueError

        logs = (session.query(Log)
            .filter(*filters)
            .order_by(Log.id.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        if not logs:
            raise HTTPException(status_code=404, detail="No matching logs found")
        else:
            return {"status_code":200, "data":logs}
    except ValueError: #Handles invalid parameters case
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception occurred for path /logs/{'level',level,'component',component,'start_time',start_time,'end_time',end_time} \nError: ",str(e))
        raise HTTPException(status_code=500, detail="Internal server error")  
    finally:
        if session:
            session.close()


@app.get("/logs/stats")
def get_logs_stats():
    session = None
    try:
        session = DBEngine().get_session()
        total = session.query(func.count(Log.id)).scalar()
        print(total)
        level_count = dict(
            session.query(Log.level, func.count(Log.id))
            .group_by(Log.level)
            .all()
        )
        component_count = dict(
            session.query(Log.component, func.count(Log.id))
            .group_by(Log.component)
            .all()
        )
        stats = {
            "total": total,
            "by_level": level_count,
            "by_component": component_count,
        }
        return {"status_code": 200, "data": stats}  
    except Exception as e:
        print(f"Exception occurred for path /logs/stats. Error: ",str(e))
        raise HTTPException(status_code=500, detail="Internal server error")    
    finally:
        if session:
            session.close()

@app.get("/logs/{log_id}")
def get_log_by_id(log_id):
    session = None
    valid_log = re.compile(r"[0-9]{14}-[0-9]+")
    try:
        if not valid_log.fullmatch(log_id):
            raise ValueError
        session = DBEngine().get_session()
        log_entry = session.get(Log, log_id)
        if log_entry:
            return {"status_code": 200, "data": log_entry}
        else:
            raise HTTPException(status_code=404, detail=f"Log record with id {log_id} not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid log id")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception occurred for path /logs/{log_id}. Error: ",str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        if session:
            session.close()

