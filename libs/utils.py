import re 


class CoreUtilsMixin:
    
    @staticmethod 
    def is_valid_email(email: str) -> bool:
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None


    @staticmethod 
    def build_json_response(msg=None, err=None, code=None, data=None, extra=None) -> dict:
        def _normalize_errors(err):
            if isinstance(err, dict):
                return {k: _normalize_errors(v) for k, v in err.items()}
            elif isinstance(err, list):
                return [_normalize_errors(v) for v in err]
            elif isinstance(err, str):
                return err 
            return str(err)

        default_response = {
            'msg': '',
            'err': '',
            'code': -1,
            'data': {}
        }
        if msg:
            default_response['msg'] = msg 
        if err:
            default_response['err'] = _normalize_errors(err)
        if code:
            default_response['code'] = code 
        if data:
            default_response['data'] = data 
        if extra and isinstance(extra, dict):
            default_response.update(**extra)
        return default_response
    