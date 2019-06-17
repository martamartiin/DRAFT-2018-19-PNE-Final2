import http.server
import socketserver
import requests
import json
from Seq import Seq
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
         json.dump(data, fp)

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.requestline, 'green')
        list_options = self.path.split('?')
        print(list_options)
        option = list_options[0]
        print(option)
        try :
            list_options = list_options[1].replace("&",";").split(";")
            json = "no"
            for element in list_options:
                if element.startswith("json"):
                    json = "yes"
        except IndexError :
            json = "no"
        if option == "/":
            f = open("menu.html", 'r')
            code = 200
            # Read the file
            contents = f.read()

            content_type = 'text/html'

        elif option == "/listSpecies":

            server = "http://rest.ensembl.org"
            ext = "/info/species?"

            try:
                limit = list_options[0][6:]
                print(limit)
                try :
                    int(limit)
                except ValueError :
                    limit = "none"
            except IndexError:
                limit = "none"
            r = requests.get(server + ext, headers={"Content-Type": "application/json"})
            decoded = r.json()
            if json == "no":
                species = "<ul>"  # having a string is more useful when creating the html file in the program
                counter = 0
                length = len(decoded["species"])
                for element in decoded["species"]:
                    species = species + "<li>" + element["display_name"]
                    species = species + "</li>"
                    counter += 1
                    if str(counter) == limit:
                        break
                f = open("limit.html", "w")
                f.write('''<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>LIST OF SPECIES</title>
                </head>
                <body style="background-color: lightpink;">
                <body>
                   The total number of species in the ensembl is : {} <br>
                   The limit you have selected is : {} <br>
                   The names of the species are : {}
                    <a href="http://localhost:8080/">A link to the index page</a>
                </body>
                </html>'''.format(len(decoded["species"]), limit, species))

                # Read the file
                f = open("limit.html", 'r')
                code = 200
                # Read the file
                contents = f.read()
                content_type = 'text/html'
            elif json == "yes" :
                path = "./"
                fileName = "limit"
                response = dict()
                response["NumberSpecies"] = len(decoded["species"])
                response["limit"] = limit
                counter = 0
                response["species"] = list()
                for element in decoded["species"] :
                     response["species"].append(element["display_name"])
                     counter += 1
                     if str(counter) == limit :
                         break
                writeToJSONFile(path, fileName, response)
                f = open("limit.json", "r")
                code = 200
                contents = f.read()
                content_type = "application/json"
        elif option == "/karyotype":

            server = "http://rest.ensembl.org"
            ext = "/info/assembly/"
            try: 
                species_selected = list_options[0][7:]
                species_selected = species_selected.replace("+", "_").lower()
                r = requests.get(server + ext + species_selected + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()
                if json == "no":
                    karyotype = ""
                    for element in decoded["karyotype"]:
                        karyotype = karyotype + "<br>" + element
                    f = open("karyotype.html", "w")
                    f.write('''<!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>KARYOTYPE OF A SPECIFIC SPECIES</title>
                                </head>
                                <body style="background-color: lightpink;">
                                <body>
                                   The chromosome´s names are : {}
                                    <a href="http://localhost:8080/">A link to the index page</a>
                                </body>
                                </html>'''.format(karyotype))

                    # Read the file
                    f = open("karyotype.html", 'r')
                    code = 200
                    contents = f.read()
                    content_type = "text/html"
                elif json == "yes":
                    path = "./"
                    fileName = "karyotype"
                    response = dict()
                    response["chromosomes"] = list()
                    for element in decoded["karyotype"] :
                        response["chromosomes"].append(element)
                    writeToJSONFile(path, fileName, response)
                    f = open("karyotype.json" , "r")
                    code = 200
                    contents = f.read()
                    content_type = "application/json"
            except KeyError:
                f = open("error_data.html", "r")
                code = 200
                contents = f.read()
                content_type = "text/html"
            except IndexError:
                f = open("error_parameters.html", "r")
                code = 200
                 # Read the file
                contents = f.read()
                content_type = 'text/html'
        elif option == "/chromosomeLength":
            try:
                species_selected = list_options[0][7:]
                species_selected = species_selected.replace("+", "_")
                chromo = list_options[1][7:].upper()
                server = "http://rest.ensembl.org"
                ext = "/info/assembly/"

                r = requests.get(server + ext + species_selected + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()
                length_chromosome = "none"
                for element in decoded["top_level_region"]:
                    if element["name"] == chromo:
                        length_chromosome = element["length"]
                if length_chromosome == "none":
                    f = open("error_data.html", "r")
                    content_type = "text/html"
                else :
                    if json == "no":
                            f = open("length.html", "w")
                            f.write('''<!DOCTYPE html>
                                                    <html lang="en">
                                                    <head>
                                                        <meta charset="UTF-8">
                                                        <title>LENGTH OF THE SELECTED CHROMOSOME</title>
                                                    </head>
                                                    <body style="background-color: lightblue;">
                                                    <body>
                                                       The length of the chromosome is :  {}
                                                       <a href="http://localhost:8080/">A link to the index page</a>
                                                    </body>
                                                    </html>'''.format(length_chromosome))

                            # Read the file
                            f = open("length.html", 'r')
                            content_type = "text/html"
                    elif json == "yes":
                        path = "./"
                        fileName = "length"
                        response = dict()
                        response["length"] = length_chromosome
                        content_type = "application/json"
                        writeToJSONFile(path, fileName, response)
                        f = open("length.json", "r")
            except IndexError:
                f = open("error_parameters.html", "r")
                content_type = "text/html"
            except KeyError:
                f = open("error_parameters.html" , "r")
                content_type = "text/html"
            code = 200
            # Read the file
            contents = f.read()
        elif option == "/geneSeq":
            try:
                gene = list_options[0][5:]
                server = "http://rest.ensembl.org"
                ext = "/homology/symbol/human/"

                r = requests.get(server + ext + gene + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()

                gene_id = decoded["data"][0]["id"]

                ext = "/sequence/id/"

                r = requests.get(server + ext + gene_id + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()
                if json== "no":
                    f = open("gene.html", "w")
                    f.write('''<!DOCTYPE html>
                                                                <html lang="en">
                                                                <head>
                                                                    <meta charset="UTF-8">
                                                                    <title>GENE`S SEQUENCE</title>
                                                                </head>
                                                                <body style="background-color: lightpink;">
                                                                <body>
                                                                   The sequence of the selected gene is :  {}
                                                                   <a href="http://localhost:8080/">A link to the index page</a>
                                                                </body>
                                                                </html>'''.format(decoded["seq"]))
                    f = open("gene.html", 'r')
                    content_type = "text/html"
                elif json == "yes":
                    path = "./"
                    fileName = "gene"
                    response = dict()
                    response["sequence"] = decoded["seq"]
                    content_type = "application/json"
                    writeToJSONFile(path, fileName, response)
                    f = open("gene.json", "r")

            except KeyError:
                f = open("error_data.html", "r")
                content_type = "text/html"
            except IndexError:
                f = open("error_parameters.html", "r")
                content_type = "text/html"
            code = 200
            # Read the file
            contents = f.read()
        elif option == "/geneInfo":
            try:
                gene = list_options[0][5:]
                server = "http://rest.ensembl.org"
                ext = "/homology/symbol/human/"

                r = requests.get(server + ext + gene + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()

                gene_id = decoded["data"][0]["id"]

                ext = "/lookup/id/"

                r = requests.get(server + ext + gene_id + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()
                start = decoded["start"]
                end = decoded["end"]
                id = decoded["id"]
                chromo = decoded["seq_region_name"]
                length = int(end) - int(start) + 1  # the "+1" is because: between 7 and 9 (both included) there are 3
                # numbers. 9-7=2 (2 + 1 = 3)
                if json == "no":
                    f = open("info.html", "w")
                    f.write('''<!DOCTYPE html>
                                                                <html lang="en">
                                                                <head>
                                                                    <meta charset="UTF-8">
                                                                    <title>INFORMATION ABOUT THE SELECTED GENE</title>
                                                                </head>
                                                                <body style="background-color: lightpink;">
                                                                <body>
                                                                   The start of the gene is :  {} <br>
                                                                   The end of the gene is : {} <br>
                                                                   The id of the gene is : {} <br>
                                                                   The length of the gene is : {} <br>
                                                                   The chromosome where the gene is located is: {}
                                                                   <a href="http://localhost:8080/">A link to the index page</a>

                                                                </body>
                                                                </html>'''.format(start, end, id, length, chromo))
                    f = open("info.html", 'r')
                    content_type = "text/html"
                elif json == "yes":
                    path = "./"
                    fileName = "info"
                    response = dict()
                    response["start"] = start
                    response["end"] = end
                    response["id"] = id
                    response["length"] = length
                    response["chromo"] = chromo
                    content_type = "application/json"
                    writeToJSONFile(path, fileName, response)
                    f = open("info.json", "r")
            except KeyError:
                f = open("error_data.html", "r")
                content_type = "text/html"
            except IndexError:
                f = open("error_parameters.html", "r")
                content_type = "text/html"
            code = 200
            # Read the file
            contents = f.read()
        elif option == "/geneCalc":
            try:
                gene = list_options[0][5:]
                server = "http://rest.ensembl.org"
                ext = "/homology/symbol/human/"

                r = requests.get(server + ext + gene + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()

                gene_id = decoded["data"][0]["id"]

                ext = "/sequence/id/"

                r = requests.get(server + ext + gene_id + "?", headers={"Content-Type": "application/json"})

                decoded = r.json()
                seq = Seq(decoded["seq"])
                if json == "no":
                    f = open("gene_calculations.html", "w")
                    f.write('''<!DOCTYPE html>
                                                                        <html lang="en">
                                                                        <head>
                                                                            <meta charset="UTF-8">
                                                                            <title>CALCULATIONS OF THE GENE</title>
                                                                        </head>
                                                                        <body style="background-color: lightpink;">
                                                                        <body>
                                                                           The total length is  :  {} <br>
                                                                           The percentage of each base is : <br>
                                                                                * A : {}  <br>
                                                                                * C : {}  <br>
                                                                                * T : {}  <br>
                                                                                * G : {}  <br>
                                                                                <a href="http://localhost:8080/">A link to the index page</a>
                                                                        </body>
                                                                        </html>'''.format(seq.len(), seq.perc("A"),
                                                                                          seq.perc("C"),
                                                                                          seq.perc("T"), seq.perc("G")))
                    f = open("gene_calculations.html", 'r')
                    content_type = "text/html"
                elif json == "yes":
                    path = "./"
                    fileName = "gene_calculations"
                    response = dict()
                    response["length"] = seq.len()
                    response["percentages"] = {"A": seq.perc("A"), "C": seq.perc("C"), "T": seq.perc("T"),
                                               "G": seq.perc("G")}
                    content_type = "application/json"
                    writeToJSONFile(path, fileName, response)
                    f = open("gene_calculations.json", "r")

            except KeyError:
                f = open("error_data.html", "r")
                content_type = "text/html"
            except IndexError:
                f = open("error_parameters.html", "r")
                content_type = "text/html"
            code = 200
            # Read the file
            contents = f.read()
        elif option == "/geneList":
            try:
                chromo = list_options[0][7:]
                start = list_options[1][6:]
                end = list_options[2][4:]
                print(end)
                print(start)
                server = "http://rest.ensembl.org"
                ext = "/overlap/region/human/"
                hola = start + "-" + end

                r = requests.get(
                    "http://rest.ensembl.org" + ext + chromo + ":" + hola + "?feature=gene;feature=transcript;feature=cds;feature=exon;",
                    headers={"Content-Type": "application/json"})

                decoded = r.json()
                print(decoded)
                if json == "no":
                    genes_sequence = "<ul>"
                    for element in decoded:
                        if element["feature_type"] == "gene":
                            try:
                                genes_sequence = genes_sequence + "<li>" + element["id"]
                                genes_sequence = genes_sequence + "</li>"
                            except TypeError:
                                genes_sequence = "None"
                    if len(decoded) == 0:
                        genes_sequence = "None"

                    f = open("gene_list.html", "w")
                    f.write('''<!DOCTYPE html>
                                                                        <html lang="en">
                                                                        <head>
                                                                            <meta charset="UTF-8">
                                                                            <title>GENES PRESENT IN THE SELECTED REGION OF THE CHROMOSOME</title>
                                                                        </head>
                                                                        <body style="background-color: lightpink;">
                                                                        <body>
                                                                           The genes present in the selected region are : <br>
                                                                           {}
                                                                           <a href="http://localhost:8080/">A link to the index page</a>
                                                                        </body>
                                                                        </html>'''.format(genes_sequence))
                    f = open("gene_list.html", 'r')
                    content_type = "text/html"
                elif json == "yes":
                    path = "./"
                    fileName = "gene_list"
                    response = dict()
                    response["genes_area"] = list()
                    for element in decoded:
                        if element["feature_type"] == "gene":
                            try:
                                response["genes_area"].append(element["id"])
                            except TypeError:
                                response["genes_area"].append("None")
                    if len(decoded) == 0:
                        response["genes_area"].append("None")
                    content_type = "application/json"
                    writeToJSONFile(path, fileName, response)
                    f = open("gene_list.json", "r")

            except KeyError:
                f = open("error_data.html", "r")
                content_type = "text/html"
            except IndexError:
                f = open("error_parameters.html", "r")
                content_type = "text/html"
            except TypeError:
                f = open("error_parameters.html", "r")
                content_type = "text/html"
            code = 200
            # Read the file
            contents = f.read()
        else:
            f = open("error.html", "r")
            code = 200
            contents = f.read()
            content_type = 'text/html'
        # Generating the response message
        self.send_response(code)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
