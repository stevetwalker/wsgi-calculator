"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback

def welcome():
    page = """
<h1>Fancy calculator</h1>
This calculator can complete the following calculations:
<ul>
    <li>add</li>
        <ul>
            <li>Example: Go to http://localhost:8080/add/5/11/4 to add 5 + 11 + 4</li>
        </ul>
    <li>subtract</li>
        <ul>
            <li>Example: Go to http://localhost:8080/subtract/2/6 to subtract 2 - 4</li>
        </ul>
    <li>multiply</li>
        <ul>
            <li>Example: Go to http://localhost:8080/multiply/7/3 to multiply 7 * 3</li>
        </ul>
    <li>divide</li>
        <ul>
            <li>Example: Go to http://localhost:8080/divide/36/2/9 to divide 36 / 2 / 9</li>
        </ul>
</ul>
"""
    return page

def add(*args):
    """ Returns a STRING with the sum of the arguments"""
    try:
        result = sum(int(x) for x in args)
        body = f"Sum: {result}"
    except (ValueError, TypeError):
        body = "Does not compute"
    return body

def subtract(*args):
    """ Returns a STRING with the difference of the arguments"""
    try:
        difference = int(args[0]) - sum(int(x) for x in args[1:])
        body = f"Difference: {difference}"
    except (ValueError, TypeError):
        body = "Does not compute"
    return body

def multiply(*args):
    """ Returns a STRING with the product of the arguments"""
    try:
        result = 1
        for arg in args:
            result *= int(arg)
        body = f"Product: {result}"
    except (ValueError, TypeError):
        body = "Does not compute"
    return body

def divide(*args):
    """ Returns a STRING with the quotient of the arguments"""
    try:
        result = None
        for arg in args:
            if result is None:
                result = int(arg)
            elif int(arg) == 0:
                raise ZeroDivisionError
            else:
                result = result / int(arg)
        body = f"Quotient: {int(result)}"
    except (ValueError, TypeError):
        body = "Does not compute"
    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': welcome,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    path = path.strip('/').split('/')
    args = path[1:]

    try:
        func = funcs[path[0]]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    status = "200 OK"

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"

    except ZeroDivisionError:
        status = "500 Internal Server Error"
        body = "<h1>Only Jack Bauer can divide by zero.<h1>"

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())

    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
