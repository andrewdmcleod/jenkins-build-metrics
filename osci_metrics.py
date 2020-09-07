import json, glob
from flask import Flask, render_template, make_response
from collections import OrderedDict
from get_build_metrics import get_build_metrics

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ugf uyfyitdy fougiuf iytfciygvc iygcycyi'

#test_date = "2020-08-27"
#file_name = "mojospecs_{}.json".format(test_date)
dated_files = glob.glob("mojospecs_2*.json")
dated_files.sort(reverse=True)

@app.route('/prometheus/')
def index():
    outline_avg = ''
    outline_high = ''
    outline_low = ''
    # for x in data:
    avg, high, low = get_build_metrics()
    for inline in avg.split("\n"):
        if inline != '':
            outline_avg = outline_avg + "osci_builds_duration_milliseconds_avg{{job_name=\"{}\", charm_name=\"{}\"}} {}\n".format(inline.split("-")[0], inline.split("-")[1], inline.split(" ")[1])
    for inline in high.split("\n"):
        if inline != '':
            outline_high = outline_high + "osci_builds_duration_milliseconds_high{{job_name=\"{}\", charm_name=\"{}\"}} {}\n".format(inline.split("-")[0], inline.split("-")[1], inline.split(" ")[1])
    for inline in low.split("\n"):
        if inline != '':
            outline_low = outline_low + "osci_builds_duration_milliseconds_low{{job_name=\"{}\", charm_name=\"{}\"}} {}\n".format(inline.split("-")[0], inline.split("-")[1], inline.split(" ")[1])
#        print(outline)
    #with open('mojospecs_output.json') as json_file:
    #    DATA = json.load(json_file, object_pairs_hook=OrderedDict)
    #for key, value in DATA.items():
    #    print(key, value)
    resp = make_response(render_template('index.html', avg=outline_avg, high=outline_high, low=outline_low))
    resp.headers['Content-type'] = 'text/plain; charset=utf-8'
    return resp
    #return render_template('index.html', data=results)


#@app.route('/<date>')
#def index_history(date):
#    # for x in data:
#    for filename in dated_files:
#        #date = filename.split("_")[1].split(".")[0]
#        file_name = "mojospecs_{}.json".format(date)
#    with open(file_name) as json_file:
#        DATA = json.load(json_file, object_pairs_hook=OrderedDict)
#    for key, value in DATA.items():
#        print(key, value)
#    return render_template('index.html', links=dated_files, data=DATA)
#

  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
