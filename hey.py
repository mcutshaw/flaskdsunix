from flask import Flask, make_response, request
from flask import render_template
import os

########################
datadir_path = '/home/pi/dsunix_data'

########################
dirlist = os.listdir(datadir_path)
for item in dirlist:
    if(item[:2] != '20'):
            dirlist.pop(dirlist.index(item))

app = Flask(__name__)
@app.route('/img/<int:vam>')
def test(vam):
    print(type(vam))
    return str(vam)
@app.route("/",methods=['GET','POST'])
def simple():
    if request.method == 'GET':
        return render_template('images_pre.html')
    elif request.method == 'POST':
        import json
        import datetime
        import matplotlib
        import StringIO
        import matplotlib.pyplot as plt
        import matplotlib.dates
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure
        from matplotlib.dates import DateFormatter
        fig = Figure()

        plt=fig.add_subplot(111)
        def validate(date_text):
            try:
                datetime.datetime.strptime(date_text, '%Y-%m-%d-%H-%M-%S')
                return True
            except ValueError:
                return False

        cwd = os.getcwd()

        date_list = []
        vim_list = []
        nano_list = []
        users_list = []

        #starting = datetime.datetime.strptime(raw_input("Start date: "),"%Y-%m-%d-%H")
        #ending = datetime.datetime.strptime(raw_input("End date: "),"%Y-%m-%d-%H")

        starting = datetime.datetime.strptime("2017-11-22-07","%Y-%m-%d-%H")
        ending = datetime.datetime.strptime("2017-11-22-08","%Y-%m-%d-%H")

        #strftime("%Y-%m-%d-%H")
        #dates = matplotlib.dates.date2num(list_of_datetimes)
        #matplotlib.pyplot.plot_date(dates, values)
        reading_file = os.path.join(cwd,str(starting.strftime("%Y-%m-%d-%H")))


        while(not starting == ending + datetime.timedelta(hours=1)):
            f = open(reading_file, "r")
            obj = json.load(f)
            f.close()


            for x in range (0, obj['num']):
                date_list.append(datetime.datetime.strptime(obj['date'][x],"%Y-%m-%d-%H-%M-%S"))
                nano_list.append(obj['nano'][x])
                vim_list.append(obj['vim'][x])
                users_list.append(obj['users'][x])

            starting+=datetime.timedelta(hours=1)
            reading_file = os.path.join(cwd,str(starting.strftime("%Y-%m-%d-%H")))

        date_list = matplotlib.dates.date2num(date_list)

        #plt.plot_date(date_list, nano_list)
        formatter = DateFormatter('%d %H:%M')

        plt.plot_date(x=date_list, y=nano_list, fmt="b-",label="nano",color="red",linewidth=1)
        plt.plot_date(x=date_list, y=users_list, fmt="b-",label="users",color="green",linewidth=1)
        plt.plot_date(x=date_list, y=vim_list,fmt="b-",label="vim",color="blue",linewidth=1)
        plt.legend()
        plt.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d-%H'))
        fig.autofmt_xdate()
        canvas=FigureCanvas(fig)
        png_output = StringIO.StringIO()
        canvas.print_png(png_output)
        response=make_response(png_output.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response
        #plt.show()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
