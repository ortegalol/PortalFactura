package org.com.mx.web;

import java.io.IOException;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller // Esta anotación indica que esta clase es un controlador de Spring MVC
public class HomeController {

    @GetMapping("/") // Esta anotación indica que este método maneja una solicitud GET a la raíz de la aplicación
    public String home() {
        return "index"; // Este método devuelve el nombre de la vista que se mostrará en el navegador (en este caso, "index")
    }

    @PostMapping("/execute")
    public String handleFormSubmission(
            @RequestParam("fecha") String fecha,
            @RequestParam("tienda") String tienda,
            @RequestParam("caja") String caja,
            @RequestParam("ticket") String ticket,
            @RequestParam("rfc") String rfc,
            @RequestParam("nombre") String nombre,
            @RequestParam("CP") String cp,
            @RequestParam("regimen") String regimen,
            @RequestParam("Cfdi") String cfdi,
            Model model
    ) {
        String command = "python C:\\Users\\edwin\\Desktop\\python\\extrae_cliente_v4.py "
                + fecha + " " + tienda + " " + caja + " " + ticket + " " + rfc + " " + nombre
                + " " + cp + " " + regimen + " " + cfdi;

        // Ejecuta el comando de Python
        try {
            Process exec = Runtime.getRuntime().exec(command);
            // Manejar la salida del proceso si es necesario
        } catch (IOException e) {
            // Manejar cualquier error al ejecutar el proceso
            e.printStackTrace();
            return "error-page"; // redirigir a una página de error
        }

        // Agregar atributos al modelo si es necesario
        model.addAttribute("mensaje", "La factura se ha generado correctamente");

        return "index"; // redirigir a una página de resultado
    }

}
