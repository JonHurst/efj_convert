import json
import configparser as cp

from efjtk.logbook import build_logbook, UnknownAircraftClass
from efjtk.config import build_config
from efjtk.expand import expand_efj
from efjtk.night import add_night_data
from efjtk.vfr import add_vfr_flag
from efjtk.ins import add_ins_flag
from efjtk.fo import add_fo_role_flag
from efjtk.summary import build as build_summary
from efj_parser import ValidationError


def logbook(in_, config):
    out = ""
    status = "failed"
    try:
        parser = cp.ConfigParser()
        parser.read_string(config)
        try:
            ac_classes = parser["aircraft.classes"]
        except KeyError:
            raise cp.Error
        out = build_logbook(in_, ac_classes)
        status = "success"
    except cp.Error:  # something fundametally wrong with ini file
        out = build_config(in_, "")
        status = "config"
    except UnknownAircraftClass:
        out = build_config(in_, config)
        status = "config"
    return out, status


_func_map = {
    "expand": expand_efj,
    "night": add_night_data,
    "vfr": add_vfr_flag,
    "fo": add_fo_role_flag,
    "ins": add_ins_flag,
}


def lambda_handler(event, context):
    data = json.loads(event["body"])
    in_ = data["efj"]
    action = data["action"]
    status = "failed"
    try:
        if action == "logbook":
            out, status = logbook(in_, data["config"])
        elif action == "summary":
            out = build_summary(in_)
            status = "success"
        elif action in _func_map:
            out = _func_map[action](in_)
            status = "success"
        else:
            out = "Not implemented"
    except ValidationError as ve:
        out = (f"efj_parser : {ve.line_number} : {ve.message}"
               f" : {ve.problem_string}")
    except Exception as e:
        out = str(e)
    return {
        'statusCode': 200,
        'body': json.dumps((out, status))
    }


if __name__ == "__main__":
    event = {
        "body": json.dumps({
            "efj": open("/home/jon/docs/logbook").read(),
            "action": "logbook",
            "config": ""
        })
    }
    print(lambda_handler(event, ""))
