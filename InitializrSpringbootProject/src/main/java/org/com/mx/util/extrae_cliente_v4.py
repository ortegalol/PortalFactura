import pyodbc as dbsqlserver
import psycopg2 as dbpostgres
import sys
from datetime import date, datetime, timedelta

if len(sys.argv) < 10:
    print("El programa necesita: fecha, tienda, caja, ticket, rfc, nombre, cp, régimen fiscal y uso cfdi")
    sys.exit(1)

p_fecha_ticket = sys.argv[1]
p_id_tienda    = sys.argv[2]
p_id_caja      = sys.argv[3]
p_folio_ticket = sys.argv[4]
p_rfc_cliente  = sys.argv[5]
p_nom_cliente  = sys.argv[6]
p_cp_cliente   = sys.argv[7]
p_rf_cliente   = sys.argv[8]
p_uso_cfdi     = sys.argv[9]

# validación fechas
#======================================================================
hoy = date.today()

fecha_inicial = p_fecha_ticket + " 00:00:00"
fecha_final   = p_fecha_ticket + " 23:59:59"

print("fecha : ", p_fecha_ticket)
print("tienda: ", p_id_tienda)
print("caja  : ", p_id_caja)
print("ticket: ", p_folio_ticket)
print("rfc:    ", p_rfc_cliente)
print("nombre: ", p_nom_cliente)
print("código postal: ", p_cp_cliente)
print("régimen fiscal: ", p_rf_cliente)
print("uso CFDI: ", p_uso_cfdi)
print("fecha inicial: ", fecha_inicial)
print("fecha final:   ", fecha_final)
print("======================================================================")

# conexión a bd
#======================================================================

cnsqlserver = dbsqlserver.connect("Driver={ODBC Driver 17 for SQL Server};"
                                  "server=172.26.31.199;"
                                  "database=Transacciones;"
                                  "UID=inter02;"
                                  "PWD=inter01;"
                                  "Trusted_Connection=no")

cnpostgres = dbpostgres.connect(user='Desarrollo',
                                password='2Tochtli',
                                host='192.163.161.30',
                                port='5432',
                                database='superissste'
                                )
cnpostgres.autocommit=True

cursor_borra   = cnpostgres.cursor()
cursor_extrae  = cnsqlserver.cursor()
cursor_inserta = cnpostgres.cursor()
cursor_inserta_cliente = cnpostgres.cursor()

query_borra = ("""DELETE FROM factura_cliente.factura_cliente
                  WHERE fecha_ticket BETWEEN %s AND %s
                  and id_tienda = %s
                  and id_caja   = %s
                  and folio_ticket = %s
                  """)

query_extrae = ("""select c.feTicket, c.idtienda, c.nofolio, c.noCaja, c.Codigo, c.iddetalle,
                   REPLACE(c.nbArticulo, ',', ''), c.noCantidad, c.mnPrecioVentaSI, c.dsImpuestoIVA,
                   d.dsMedida, e.sat, e.unidad_medida, c.mnPrecioVenta, c.dsImpuestoIEPS
                   from kdTicketArticulo c,
                        cArticulo d,
                        codigosSAT e,
                        kticket f
                   where c.feticket between ? and ?
					 and c.idtienda =  ?
					 and c.nocaja =  ?
					 and CAST(c.nofolio AS int) =  ?
                     and d.Codigo = c.Codigo
                     and e.sku = cast(c.codigo as varchar)
                     and f.idtienda = c.idtienda
                     and f.feticket = c.feticket
                     and f.nocaja = c.nocaja
                     and f.nofolio = c.nofolio
                     and f.dstipotransaccion = 'Venta'
                     --and CAST(c.nofolio AS int) not in (select nofolio from kticketfacturado
                     --                                   where idtienda = c.idtienda
                     --                                     and feticket = c.feticket
                     --                                     and nocaja = c.nocaja
                     --                                     and nofolio = CAST(c.nofolio AS int) )
                     and CAST(c.nofolio AS int) not in (select nofolioventa from kticketdevolucion
                                                        where idtienda = c.idtienda
                                                          and feticketventa = c.feticket
                                                          and nocaja = c.nocaja
                                                          and nofolioventa = CAST(c.nofolio AS int) )
                     order by 1, 2, 3, 6

                     """)

query_inserta = ("""INSERT INTO factura_cliente.factura_cliente
                    (fecha_ticket, id_tienda, folio_ticket, id_caja, id_articulo, 
                     num_consecutivo_articulo, nom_articulo, cantidad, precio, iva,
                     unidad_medida, id_articulo_sat, unidad_medida_sat, precio_venta, 
                     ieps) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

query_inserta_cliente = ("""INSERT INTO factura_cliente.factura_cliente_xml
                    (fecha_ticket, id_tienda, id_caja, folio_ticket, rfc_cliente, nom_cliente, cp_cliente, rf_cliente, uso_cfdi)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")

print("Inicia Proceso ...")
param = (fecha_inicial, fecha_final, p_id_tienda, p_id_caja, p_folio_ticket)
print(param)

cursor_borra.execute(query_borra, param)
cursor_extrae.execute(query_extrae, param)

i=0
for fila in cursor_extrae:
    fecha_ticket      = fila[0]
    id_tienda         = fila[1]
    folio_ticket      = fila[2]
    id_caja           = fila[3]
    id_articulo       = fila[4]
    num_consecutivo_articulo = fila[5]
    nom_articulo      = fila[6]
    cantidad          = fila[7]
    precio            = fila[8]
    iva               = fila[9]
    unidad_medida     = fila[10]
    id_articulo_sat   = fila[11]
    unidad_medida_sat = fila[12]
    precio_venta      = fila[13]
    ieps              = fila[14]

    param_inserta = (fecha_ticket, id_tienda, folio_ticket, id_caja, id_articulo,
                     num_consecutivo_articulo, nom_articulo, cantidad, precio, iva,
                     unidad_medida, id_articulo_sat, unidad_medida_sat, precio_venta,
                     ieps)

    print(f'{fecha_ticket}, {id_tienda}, {folio_ticket}, {id_caja}, {id_articulo}, {num_consecutivo_articulo}, {nom_articulo}, {cantidad}, {precio}, {iva}, {unidad_medida}, {precio_venta}')


    cursor_inserta.execute(query_inserta, param_inserta)

    i+=1

print(f'Registros Extraídos: {i} ')

if i>0:
   param_inserta_cliente = (fecha_ticket, id_tienda,id_caja, folio_ticket, p_rfc_cliente, p_nom_cliente, p_cp_cliente, p_rf_cliente, p_uso_cfdi)
   cursor_inserta_cliente.execute(query_inserta_cliente, param_inserta_cliente)

cursor_borra.close()
cursor_extrae.close()
cursor_inserta.close()
cursor_inserta_cliente.close()
cnsqlserver.close()
cnpostgres.close()
