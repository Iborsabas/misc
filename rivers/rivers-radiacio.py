import csv

data = csv.reader(open('spr.csv'), delimiter=',')
rivers = {}

# Guardamos los rios en un hash para acceder mas rapidamente
for d in data:
    try:
        int(d[0])
        rivers[d[0]] = d
    except ValueError:
        pass


def find_rivers_rec(id, river, ends=False, way={}):
    """
    Encuentra recursivamente el curso de un rio
    """
    dest = river[1]
    if dest == id:
        return True, way
    elif dest and dest not in way and dest in rivers:
        way[dest] = river
        return find_rivers_rec(id, rivers[dest], False, way)
    else:
        return False, {}


def find_rivers_wrtfile(f,id):
    """
    Encuentra todos los rios que desembocan directa o indirectamente en el rio id
    """
    if not rivers.has_key(id):
        print "ERROR: Ese rio no existe :-("
    else:
        enders = []
        for k, v in rivers.iteritems():
            if k != id:
                ends, way = find_rivers_rec(id, v, way={})
                if ends:
                    enders.append(k)
        all_floats = False
        for float_field in [3, 5, 7, 9, 11]:#Son les columnes que es volen calcular
            try:
                float(rivers[id][float_field])
            except ValueError:
                print ValueError("Faltan datos para el rio {}".format(str(id)))
            else:
                all_floats = True
        if all_floats:
            f.write(id)
            f.write(';')
            totalcatchment = float(rivers[id][3]) + sum(float(rivers[k][3]) for k in enders)
            f.write(str(totalcatchment))
            f.write(';')
            srt = float(rivers[id][5])*float(rivers[id][3]) + sum(float(rivers[k][5]) * float(rivers[k][3])for k in enders)
            f.write(str(srt/totalcatchment))
            f.write(';')
            dird = float(rivers[id][7])*float(rivers[id][3]) + sum(float(rivers[k][7]) * float(rivers[k][3])for k in enders)
            f.write(str(dird/totalcatchment))
            f.write(';')
            difd = float(rivers[id][9])*float(rivers[id][3]) + sum(float(rivers[k][9]) * float(rivers[k][3])for k in enders)
            f.write(str(difd/totalcatchment))
            f.write(';')
            durd = float(rivers[id][11])*float(rivers[id][3]) + sum(float(rivers[k][11]) * float(rivers[k][3])for k in enders)
            f.write(str(durd/totalcatchment))
            f.write('\n')

########################### MAIN
            #Escriu els resultats en la taula
f = open('sprt.csv','w')#Crea taula de radiacions totals
f.write('CODI_BASE;tc;srt;dirt;dift;durt\n')#Escriu les columnes
for id in rivers.keys():
    find_rivers_wrtfile(f,id)
f.close()
