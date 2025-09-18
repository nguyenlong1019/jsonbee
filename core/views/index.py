from django.shortcuts import render 
from django.views import View 
from django.http import JsonResponse 
import uuid, json, ast # ast: abstract syntax tree https://docs.python.org/3.10/library/ast.html
from libs.utils import CoreUtilsMixin


class IndexView(View, CoreUtilsMixin):
    template_name = 'core/index.html'


    def get(self, request, *args, **kwargs):
        if not request.session.get('jbid'):
            request.session['jbid'] = str(uuid.uuid4())

        return render(request, self.template_name, status=200)
    

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse(self.build_json_response(err=str(e)), status=400)
        
        json_input = data.get('json_input')

        try:
            parsed_dict = ast.literal_eval(json_input)
        except Exception as e:
            try:
                parsed_dict = json.loads(json_input)
            except Exception as e:
                parsed_dict = self.smart_json_parse(json_input)
                if not parsed_dict:
                    return JsonResponse(self.build_json_response(err=f"Invalid json or python dict: {str(e)}"), status=400)

        formatted_json = json.dumps(parsed_dict, indent=4, ensure_ascii=False, default=str)

        request.session["last_input"] = json_input 
        
        return JsonResponse(self.build_json_response(
            msg='Success',
            code=0,
            data={
                'jo': formatted_json
            }
        ), status=200) 
