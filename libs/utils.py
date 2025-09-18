import re 
import json 


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
    

    @staticmethod 
    def smart_json_parse(json_input: str):
        """
        Try to parse a slightly malformed JSON string by auto-fixing common issues.
        Return False if fails
        """
        fixed_input = json_input

        # Step 1: Fix common unescaped double quote inside value 
        fixed_input = re.sub(
            r'("formatted_value"\s*:\s*)"([^"]+)"\s*\(([^)]+)\)"',
            lambda m: f'{m[1]}"{m[2]} ({m[3]})"',
            fixed_input
        )

        # Step 2: Remove any control characters (like \x00 - \x1F)
        fixed_input = re.sub(r'[\x00-\x1f]+', '', fixed_input)

        # Step 3: Escape standalone unescaped backslashes 
        fixed_input = re.sub(r'(?<!\\)\\(?![\\/"bfnrtu])', r'\\\\', fixed_input)

        # Step 4: Escape quotes inside values if needed 
        def escape_quotes_in_values(match):
            key = match.group(1)
            value = match.group(2)
            value = value.replace('"', '\\"')  # escape all quotes inside
            return f'"{key}": "{value}"'
    
        try:
            return json.loads(fixed_input)
        except Exception as e:
            return False 

