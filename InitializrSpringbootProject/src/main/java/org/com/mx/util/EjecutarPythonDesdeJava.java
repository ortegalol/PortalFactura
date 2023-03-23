package org.com.mx.util;

import java.io.*;
import javax.swing.JOptionPane;

public class EjecutarPythonDesdeJava {
    public static void main(String[] args) {
        try {
            // Solicita los valores de las variables al usuario utilizando JOptionPane
            String fecha = JOptionPane.showInputDialog(null, "Ingrese la fecha (YYYY-MM-DD):");
            String tienda = JOptionPane.showInputDialog(null, "Ingrese la tienda:");
            String caja = JOptionPane.showInputDialog(null, "Ingrese la caja:");
            String ticket = JOptionPane.showInputDialog(null, "Ingrese el número de ticket:");
            String rfc = JOptionPane.showInputDialog(null, "Ingrese el RFC:");
            String nombre = JOptionPane.showInputDialog(null, "Ingrese el nombre del cliente:");
            String cp = JOptionPane.showInputDialog(null, "Ingrese el código postal:");
            String regimen = JOptionPane.showInputDialog(null, "Ingrese el régimen fiscal:");
            String cfdi = JOptionPane.showInputDialog(null, "Ingrese el tipo de comprobante (Cfdi):");

            // Construye el comando de ejecución del script de Python utilizando los valores ingresados
            ProcessBuilder pb = new ProcessBuilder("python", "C:\\Users\\edwin\\Desktop\\Scripts\\extrae_cliente_v4.py", fecha, tienda, caja, ticket, rfc, nombre, cp, regimen, cfdi);

            // Ejecuta el script de Python
            Process proceso = pb.start();
            
            // Obtiene la salida del proceso y la muestra en la consola
            InputStream is = proceso.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String linea;
            System.out.println("Salida del script de Python:");
            while ((linea = br.readLine()) != null) {
                System.out.println(linea);
            }
            
            // Espera a que el proceso termine
            int resultado = proceso.waitFor();
            System.out.println("El script de Python ha terminado con resultado: " + resultado);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
