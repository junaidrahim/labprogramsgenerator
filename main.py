import flask
import os, json, random
from zipfile import ZipFile



def writeAllData(name, hostel, data):
    dirName = "dump/programs"+ name +str(random.randint(1,100000))
    os.mkdir(dirName)

    for directory in [*data]:
        thisDir = dirName + "/" + directory
        os.mkdir(thisDir)

        for f in [*data[directory]]:
            k = open(thisDir + '/' + f, 'w')

            if(f == "program2_name_And_Address.c"):
                code = str(data[directory][f])
                code = code.replace("Junaid", name)
                code = code.replace("KP7(B)", hostel)
                k.write(code)

            else:
                k.write(data[directory][f])
            
            k.close()

    return dirName


def get_all_file_paths(directory): 
    file_paths = [] 
  
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    return file_paths  

server = flask.Flask(__name__)

@server.route("/", methods=['GET'])
def index():
    return flask.render_template("index.html")

@server.route("/download", methods=['POST'])
def download():
    name = flask.request.form["nameInput"]
    hostel = flask.request.form["hostelInput"] 

    data = json.loads(open('data.json','r').read())
    
    dirName = writeAllData(str(name), str(hostel), data)
    filepaths = get_all_file_paths(dirName)

    with ZipFile('{}.zip'.format(dirName),'w') as zip: 
        # writing each file one by one 
        for file in filepaths: 
            zip.write(file)

    return flask.send_file('{}.zip'.format(dirName), as_attachment=True)


if __name__=="__main__":
    server.run(port=8000, host='0.0.0.0', debug=True)