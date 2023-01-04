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