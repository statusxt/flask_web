from flask import Flask
from flask import render_template
import subprocess
import telnetlib
import urllib

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

app = Flask(__name__)

def top_menu():
    pass

def call_proc(cmd):
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return output

def filter_output(output, host):
    o_filter = ""
    for line in output.stdout:
        o_filter = o_filter+str(line, 'utf-8')

    return_data = "%s" % host + " " +  o_filter
    return return_data

@app.route('/')
def index():
    return render_template('center.html', return_data='Home Page')

@app.route('/ping/')
@app.route('/ping/<host>')
@app.route('/pong/<host>', alias=True)
def ping(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "ping -c 4 %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/tracert/')
@app.route('/traceroute/')
@app.route('/traceroute/<host>')
@app.route('/tracert/<host>', alias=True)
def traceroute(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "traceroute -m 10 %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)


@app.route('/dns-lookup/')
@app.route('/lookup/')
@app.route('/dns-lookup/<host>')
@app.route('/lookup/<host>', alias=True)
def dns_lookup(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "nslookup %s 8.8.8.8" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/whois/')
@app.route('/whois/<host>')
def whois(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "whois %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.errorhandler(403)
def forbidden():
    return render_template('center.html', return_data='Can\'t do that!' )

@app.errorhandler(404)
def page_not_found():
    return render_template('center.html', return_data='Nothing found here!')

@app.errorhandler(500)
def internal_server():
    return render_template('center.html', return_data='Something smells strange!')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
