package ciclo4.grupo37.misiontic.org.MainSecurity.controladores;

import ciclo4.grupo37.misiontic.org.MainSecurity.modelos.Rol;
import ciclo4.grupo37.misiontic.org.MainSecurity.modelos.Usuario;
import ciclo4.grupo37.misiontic.org.MainSecurity.repositorios.RepositorioRol;
import ciclo4.grupo37.misiontic.org.MainSecurity.repositorios.RepositorioUsuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/usuarios")
public class ControladorUsuario {
    @Autowired
    private RepositorioUsuario miRepositorioUsuario;
    @Autowired
    private RepositorioRol miRepositorioRol;

    @GetMapping("")
    public List<Usuario> index(){
        return miRepositorioUsuario.findAll();
    }

    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping
    public Usuario create(@RequestBody Usuario infoUsuario){
        infoUsuario.setContrasena(convertirSHA256(infoUsuario.getContrasena()));
        return miRepositorioUsuario.save(infoUsuario);
    }

    @GetMapping("{id}")
    public Usuario show(@PathVariable String id){
        Usuario usuarioActual = miRepositorioUsuario.findById(id).orElse(null);
        return usuarioActual;
    }

    @PutMapping("{id}")
    public Usuario update(@PathVariable String id, @RequestBody Usuario infoUsuario){
        Usuario usuarioActual = miRepositorioUsuario.findById(id).orElse(null);
        if(usuarioActual!=null){
            usuarioActual.setSeudonimo(infoUsuario.getSeudonimo());
            usuarioActual.setCorreo(infoUsuario.getCorreo());
            usuarioActual.setContrasena(convertirSHA256(infoUsuario.getContrasena()));
            return miRepositorioUsuario.save(usuarioActual);
        }else{
            return null;
        }
    }
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @DeleteMapping("{id}")
    public void delete(@PathVariable String id){
        Usuario usuarioActual = miRepositorioUsuario
                .findById(id)
                .orElse(null);
        if(usuarioActual!=null){
            miRepositorioUsuario.delete(usuarioActual);
        }
    }

    /**
     * Función que añade un rol a un usuario
     * */
    @PutMapping("{id_usuario}/rol/{id_rol}")
    public Usuario asignarRolUsuario(@PathVariable String id_usuario,
                                     @PathVariable String id_rol){
        Usuario usuarioActual = miRepositorioUsuario
                .findById(id_usuario)
                .orElse(null);
        Rol rolActual = miRepositorioRol
                .findById(id_rol)
                .orElse(null);
        if(usuarioActual!=null && rolActual!=null){
            usuarioActual.setRol(rolActual);
            return miRepositorioUsuario.save(usuarioActual);
        }else{
            return null;
        }
    }

    /**
     * Añadimos una función para manejar el encriptado de las
     * contraseñas
     * */
    public String convertirSHA256(String password){
        MessageDigest md = null;
        try{
            md = MessageDigest.getInstance("SHA-256");
        }catch (NoSuchAlgorithmException e){
            e.printStackTrace();
            return null;
        }
        byte[] hash = md.digest(password.getBytes());
        StringBuffer sb = new StringBuffer();
        for(byte b: hash){
            sb.append(String.format("%20x", b));
        }
        return sb.toString();
    }

    /**
     * Validar el ingreso de algún usuario
     * */

    @PostMapping("/validar")
    public Usuario validate(@RequestBody Usuario infoUsuario,
                            final HttpServletResponse response)
    throws IOException {
        Usuario usuarioActual = miRepositorioUsuario.getUserByMail(infoUsuario.getCorreo());
        Usuario usuarioPorSeudonimo = miRepositorioUsuario.getUserBySeudonimo(infoUsuario.getSeudonimo());
        if(usuarioActual != null && usuarioActual.getContrasena()
                .equals(convertirSHA256(infoUsuario.getContrasena()))
                && usuarioPorSeudonimo.getSeudonimo() != null){
            usuarioActual.setContrasena((""));
            return usuarioActual;
        }else{
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return null;
        }

    }

}
