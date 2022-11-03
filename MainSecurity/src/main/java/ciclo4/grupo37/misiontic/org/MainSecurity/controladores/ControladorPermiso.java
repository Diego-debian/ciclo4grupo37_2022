package ciclo4.grupo37.misiontic.org.MainSecurity.controladores;

import ciclo4.grupo37.misiontic.org.MainSecurity.modelos.Permiso;
import ciclo4.grupo37.misiontic.org.MainSecurity.repositorios.RepositorioPermiso;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/permisos")
public class ControladorPermiso {
    @Autowired
    private RepositorioPermiso miRepositorioPermiso;

    @GetMapping("")
    public List<Permiso> index(){
        return miRepositorioPermiso.findAll();
    }

    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping
    public Permiso create(@RequestBody Permiso infoPermiso){
        return miRepositorioPermiso.save(infoPermiso);
    }

    @GetMapping("{id}")
    public Permiso show(@PathVariable String id){
        Permiso permisoActual = miRepositorioPermiso.findById(id)
                .orElse(null);
        return permisoActual;
    }

    @PutMapping("{id}")
    public Permiso update(@PathVariable String id, @RequestBody Permiso infoPermiso){
        Permiso permisoActual = miRepositorioPermiso.findById(id)
                .orElse(null);
        if(permisoActual != null){
            permisoActual.setMetodo(infoPermiso.getMetodo());
            permisoActual.setUrl(infoPermiso.getUrl());
            return miRepositorioPermiso.save(permisoActual);
        }else{
            return null;
        }
    }

    @ResponseStatus(HttpStatus.NO_CONTENT)
    @DeleteMapping("{id}")
    public void delete(@PathVariable String id){
        Permiso permisoActual = miRepositorioPermiso.findById(id)
                .orElse(null);
        if(permisoActual!=null){
            miRepositorioPermiso.delete(permisoActual);
        }
    }

}
