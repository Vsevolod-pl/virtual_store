import json

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

with open('data.json', 'r') as f:
    data = json.load(f)

style_thing = '''
<style>
details > summary {
  padding: 4px;
  border: none;
  cursor: pointer;
}

details > p {
  padding: 4px;
  margin: 0;
}
</style>
'''

js_functions = '''
<script>
function add_item(name, cost, path) {
    let form = document.getElementById('buying_form');
    let listofthings = form.getAttribute('listofthings')
    if (listofthings === null) {
        listofthings = [];
    } else {
        listofthings = JSON.parse(listofthings);
    }
    if (!listofthings.includes(name)){
        let div = document.createElement('div');
        form.append(div);
        let inp_num = document.createElement('input');
        inp_num.setAttribute('type', 'number');
        inp_num.setAttribute('name', 'number');
        inp_num.setAttribute('value', 1);
        inp_num.setAttribute('style', 'display:inline-block; width:30%');
        div.append(inp_num);
        let inp_name = document.createElement('input');
        inp_name.setAttribute('type', 'text');
        inp_name.setAttribute('value', name);
        inp_name.setAttribute('name', 'name');
        inp_name.setAttribute('readonly', 'readonly');
        inp_name.setAttribute('style', 'display:inline-block; width:50%');
        div.append(inp_name);
        let inp_path = document.createElement('input');
        inp_path.setAttribute('type', 'text');
        inp_path.setAttribute('value', path);
        inp_path.setAttribute('name', 'path');
        inp_path.setAttribute('readonly', 'readonly');
        inp_path.setAttribute('style', 'display:none; width:0%');
        div.append(inp_path);
        let inp_cost = document.createElement('input');
        inp_cost.setAttribute('type', 'text');
        inp_cost.setAttribute('value', cost);
        inp_cost.setAttribute('name', 'cost');
        inp_cost.setAttribute('readonly', 'readonly');
        inp_cost.setAttribute('style', 'display:inline-block; width:20%');
        div.append(inp_cost);
        listofthings.push(name);
        form.setAttribute('listofthings', JSON.stringify(listofthings));
    }
}
</script>'''


def diclis2htm(diclis, nest_level=0, path_to_thing=[]):
    res = ''
    path_to_thing = path_to_thing.copy()
    
    if type(diclis) is dict:
        
        if not diclis['visible']:
            return ''
        
        if 'itemtype' in diclis:
            res = '<div style="display:inline-block">'
            res += '<details>\n<summary>'
            res += '_'*nest_level*0 + diclis['name'] + '    cost: ' + str(diclis['cost'])
            res += '</summary>\n'
            res += '<div style="width: 50%; float:left">\n'
            for key in diclis:
                if key != 'visible' and key != 'itemtype' and key != 'name' and key != 'cost' and key != 'img_url' and key != 'description':
                    res += f'<p><b>{key}</b>: {diclis[key]}</p>'
            
            res += '</div>\n<div style="width: 50%; float:right">\n'
            if 'img_url' in diclis:
                img_url = diclis['img_url']
                res += f'<img src={img_url} style="width: 100%">\n'
            description = diclis['description']
            res += f'<p><b>Description:</b>\n{description}</p>'
            
            name = diclis['name']
            cost = diclis['cost']
            path = json.dumps(path_to_thing)
            path = path.replace('"', "\\'")
            res += f'<button onclick="add_item(\'{name}\', {cost}, \'{path}\')">Add to list</button>'
            
            res += '</div>\n'
            
            res += '</details>\n</div>\n'
            return res
        
        for key in diclis:
            if key != 'visible':
                if (type(diclis[key]) is dict and 'itemtype' in diclis[key]):
                    res += '<p>\n' + diclis2htm(diclis[key], nest_level+1, path_to_thing+[key]) + '</p>\n'
                else:
                    res += '<details>\n<summary>' + '_'*nest_level*4 + key + '</summary>\n'
                    res += diclis2htm(diclis[key], nest_level+1, path_to_thing+[key])
                    res += '</details>\n'
        return res
    elif type(diclis) is list:
        i = 0
        for item in diclis:
            i += 1
            res += '<p>\n' + diclis2htm(item, nest_level, path_to_thing+[i]) + '</p>\n'
            
        return res
    else:
        return str(diclis) + '\n'


def magaz(request):
    res = '<html>' + style_thing + js_functions + '<body>\n'
    res += '<div style="width: 80%; float:left; display:inline-block">'
    res += diclis2htm(data)
    res += '</div><div style="width: 17%; float:right; display:inline-block">'
    res += '<form id="buying_form" action="/magaz_backend">'
    res += '<input type="submit" value="Оформить покупку" style="width: 100%;">\n'
    res += '</form></div>'
    res += '</body></html>'
    
    return Response(res)


def get_from_path(data, path):
    if path:
        return get_from_path(data[path[0]], path[1:])
    else:
        return data.copy()


bought_nothing = '''<html><body>
<h1>You've bought nothing.
:(</h1>
</body></html>'''



def magaz_backend(request):
    paths = request.GET.getall('path')
    if not paths:
        return bought_nothing
    
    paths = [json.loads(path.replace("'", '"')) for path in paths]
    listofthings = [get_from_path(data, path) for path in paths]
    nums = [max(int(i), 0) for i in request.GET.getall('number')]
    cost = 0
    for i, item in enumerate(listofthings):
        cost += item['cost']*nums[i]
        item['cost'] = '\t'+str(item['cost']) + f'$, {nums[i]} штукей'
    res = '<html>' + style_thing + '<body>\n'
    res += f'<h1>You have to pay: {cost}$</h1>'
    res += '<div style="width: 80%; left:50%; display:inline-block">'
    
    res += diclis2htm(listofthings)
    res += '</div>'
    res += '</body></html>'
    return Response(res)



with Configurator() as config:
    config.add_route('magaz', '/magaz')
    config.add_view(magaz, route_name='magaz')
    config.add_route('magaz_backend', '/magaz_backend')
    config.add_view(magaz_backend, route_name='magaz_backend')
    config.add_static_view(name='images', path='./images')
    app = config.make_wsgi_app()
server = make_server('0.0.0.0', 6543, app)
server.serve_forever()