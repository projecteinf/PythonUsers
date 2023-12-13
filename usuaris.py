import sys
import logging
import os
import subprocess

def crearDirectory():
    if not os.path.exists("/etc/usuaris"): 
        os.makedirs("/etc/usuaris")

def dadesValides(arguments):
    inici=4
    if arguments[4] == "--cap":
        inici=5 
        """  """   
    for i in range(inici, len(arguments),2):
        if arguments[i] not in ["--mail", "--phone", "--mobile", "--posicio"]:
            return False    
    
    return True


def prepararDades(arguments):
    dades = {}

    dades["nomUsuari"] = arguments[1]
    dades["nomComplet"] = arguments[2]
    dades["departament"] = arguments[3]

    inici=4
    dades["--cap"] = False

    if arguments[4] == "--cap":
        dades["--cap"] = True
        inici=5

    for i in range(inici, len(arguments),2):
        dades[arguments[i]] = arguments[i+1]
        
    return dades

def crearUsuari(nomUsuari):
    return os.system("useradd -m "+nomUsuari)    

def afegirGrup(nomUsuari):
    return os.system("usermod -a -G capdept "+nomUsuari) 
            
def guardarDades(dades, fileName):
    with open(fileName, 'w') as f:
        for key, value in dades.items():
            if "--" in key:
                key = key[2:]
            f.write(key.upper() + ":" + str(value)+"\n")

def esDelDepartament(departament):
    pot = 2

    if os.environ.get('SUDO_USER') == None:
        return 1

    if os.path.exists("/etc/usuaris/"+currentUser+".dat"):
        deptUserCreator=subprocess.check_output('grep ^DEPARTAMENT: '+"/etc/usuaris/"+currentUser+".dat"+' | cut -d":" -f2',shell=True)
        deptUserCreator=deptUserCreator.decode("utf-8").rstrip()
        if deptUserCreator == departament:
            pot = 0

    return pot   

if __name__ == "__main__":
    
    """ 
        python3 usuaris.py nomUsuari nomComplet departament [opcions]
        opcions:
            --mail correuElectronic
            --phone numeroTelefon
            --mobile numeroMobil
            --posicio carrec 

        Exemple:
            python3 usuaris.py jordi "Jordi Masip" "Informàtica" --mail jmasip@inf.local
            python3 usuaris.py jordi "Jordi Masip" "Informàtica" --mail jmasip@inf.local --mail jmasip@info.com
    """

    logging.basicConfig(
        filename='/var/log/usuaris.log',level=logging.INFO, 
        format='%(asctime)s %(levelname)s %(message)s')

    currentUser=os.environ.get('SUDO_USER')
    if currentUser == None:
        currentUser=os.environ.get('USER')
      

    number_of_arguments = len(sys.argv)-1
    if number_of_arguments < 3:
        print ("USAGE: python3 usuaris.py nomUsuari nomComplet departament [opcions]")
        logging.warning(currentUser+" USAGE: "+str(sys.argv))
        sys.exit(1)


    if not dadesValides(sys.argv):
        print ("USAGE: python3 usuaris.py nomUsuari nomComplet departament [opcions]")
        logging.warning(currentUser+" USAGE: "+str(sys.argv))
        sys.exit(1)

    
    crearDirectory()

    dades=prepararDades(sys.argv)

    if not dades["--cap"]:    # Usuari root només pot crear usuaris de cap de departament
        potCrear=esDelDepartament(dades["departament"]) 
        if potCrear == 2:
            print("No pots crear usuaris del departament "+dades["departament"])
            logging.warning(currentUser+" No pots crear usuaris del departament "+dades["departament"])
            sys.exit(2)
        elif potCrear == 1:
            print("Usuari només pot crear caps de departament")
            sys.exit(4)

    ok = crearUsuari(dades["nomUsuari"])
    if dades["--cap"]:
        ok = afegirGrup(dades["nomUsuari"])

    if ok != 0:
        print("Error creant usuari "+dades["nomUsuari"])
        logging.warning(currentUser+" Error creant usuari "+dades["nomUsuari"])
        sys.exit(3)

    fileName = "/etc/usuaris/"+dades["nomUsuari"]+".dat"
    guardarDades(dades, fileName)
    
      
    logging.info(currentUser+" Creat usuari "+dades["nomUsuari"])
    
    
