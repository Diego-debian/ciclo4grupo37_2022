package ciclo4.grupo37.misiontic.org.MainSecurity.repositorios;

import ciclo4.grupo37.misiontic.org.MainSecurity.modelos.Rol;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface RepositorioRol extends MongoRepository<Rol, String > {
}
