function logout() {
    var form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', "{% url 'logout' %}");

    var csrf = document.createElement('input');
    csrf.setAttribute('type', 'hidden');
    csrf.setAttribute('name', 'csrfmiddlewaretoken');
    csrf.setAttribute('value', '{{ csrf_token }}');
    form.appendChild(csrf);

    document.body.appendChild(form);
    form.submit();
}