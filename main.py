import bs4
from colorama import Fore
from bs4 import BeautifulSoup as Soup
from os.path import exists
from shutil import rmtree
from os import mkdir
from os import listdir
class OpenPlcParser():
    def __init__(self,path:str):
        with open(path,mode="r",encoding="utf-8") as openplc_file:
            content=openplc_file.read()
        self.__document=Soup(content,"xml")
        self.__project:bs4.Tag=self.__document.project
    def showStructure(self):
        topLevel=[item for item in self.__project.instances.configurations.configuration.resource.addData.children]
        for item in topLevel:
            # if item.name=="pouInstance"
            print(item.name)
            # pous=[pou for pou in item.children if pou.name is not None]
            # for pou in pous:
            #     print(pou.name)
        # pous=self.__project.find_all("pou")
        # item:bs4.Tag
        # for pou in pous:
        #     print(pou.parent.parent.parent.parent.parent.parent.name)

    def findElements(self):
        tags=self.__project.find_all("pou")
        if exists("D://parse//POUS"):
            rmtree("D://parse//POUS")
        mkdir("D://parse//POUS")

        for tag in tags:
            with open(f"D://parse//POUS//{tag['name']}.xml",mode="w",encoding="utf-8") as tag_file:
                tag_file.write(str(tag))
                tag_file.flush()
                tag_file.close()
            print("{0} -- {1}".format(tag.name,tag["name"]))
            parent=tag.parent
            stub=self.__document.new_tag("stub")
            stub["name"]=tag["name"]
            tag.decompose()
            parent.append(stub)
    def saveAll(self):
        with open("D://parse//clear.xml",mode="w",encoding="utf-8") as file:
            file.write(str(self.__document))
            file.flush()
            file.close()

    def parseAll(self):
        with open("D://parse//clear.xml",mode="r",encoding="utf-8") as clear_file:
            content=clear_file.read()
        result_xml=Soup(content,"xml")

        print(Fore.RED+"Создал Суп для clear.xml")
        stubs=result_xml.find_all("stub")

        for filename in listdir("D://parse//POUS"):

            print( Fore.GREEN+f"Разбираю {filename} ")
            with open(f"D://parse//POUS//{filename}",mode="r") as tag_file:
                content=tag_file.read()
                tag_file.close()
            xml=Soup(content,"xml")
            for stub in stubs:
                # print(type(stub))
                # print(Fore.WHITE+f"{stub['name']}=={xml.pou['name']}")
                #if type(stub["name"]) is not None and type(xml.pou['name'] is not None):
                print(f"1:{type(stub['name'])} 2:{type(xml.pou['name'])}")
                if stub["name"]==xml.pou["name"]:
                    print("Здесь все ломается")
                    parent=stub.parent
                    parent.append(xml)


        with open(f"D://parse//output.xml",mode="w",encoding="utf-8") as output_file:
            output_file.write(str(result_xml))
            output_file.flush()
            output_file.close()

    def countObjects(self):
        with open("D://parse//clear.xml",mode="r",encoding="utf-8") as clear_file:
            content=clear_file.read()
        clearxml=Soup(content,"xml")
        stubs=clearxml.find_all("stub")
        print(stubs.__len__())
        print(listdir("D://parse//POUS").__len__())

    def buildNewXml(self):
        with open("D://parse//clear.xml", mode="r", encoding="utf-8") as clear_file:
            content = clear_file.read()
            clear_file.close()
        result_xml = Soup(content, "xml")

        stubs = result_xml.find_all("stub")

        for stub in stubs:
            print(stub['name'])
            for filename in listdir("D://parse//POUS"):
                with open(f"D://parse//POUS//{filename}", mode="r") as tag_file:
                    content = tag_file.read()
                    tag_file.close()
                xml = Soup(content, "xml")
                if stub["name"] == xml.pou["name"]:
                    parent = stub.parent
                    parent.append(xml)

        with open(f"D://parse//output.xml",mode="w",encoding="utf-8") as output_file:
            output_file.write(str(result_xml))
            output_file.flush()
            output_file.close()

    def clearStubs(self):
        with open("D://parse//output.xml", mode="r", encoding="utf-8") as clear_file:
            content = clear_file.read()
            clear_file.close()
        result_xml = Soup(content, "xml")
        stubs = result_xml.find_all("stub")

        for stub in stubs:
            stub.decompose()

        with open(f"D://parse//output.xml", mode="w", encoding="utf-8") as output_file:
            output_file.write(str(result_xml))
            output_file.flush()
            output_file.close()








if __name__ == '__main__':
    parser=OpenPlcParser("D://parse//Device-1.xml")
    #parser.showStructure()
    #parser.findElements()
    #parser.saveAll()
    #parser.parseAll()
    parser.buildNewXml()
    parser.clearStubs()
    #parser.countObjects()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
