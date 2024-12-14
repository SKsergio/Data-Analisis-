import requests
import pandas as pd

# clase padre, esta tendra la url base sobre la cual giraran las consultas que hagamos a la BD
class MainClassMovie:
    url_base = "https://api.themoviedb.org/3/"
    API_key = "56730a8114515a93bf2ec1a7448fcae0"
    Messagen = ''

    # devolver la url y la api key
    def getUrlBase(self):
        return self.url_base

    def getKey(self):
        return self.API_key
    

class MoviesGenere(MainClassMovie):
    def __init__(self):
        super().__init__()
        self.generos = []  # Atributo para almacenar los géneros

    def getGenderMovies(self):
        Url = self.getUrlBase()
        key = self.getKey()
        params = {"api_key": key, "language": "es-ES"}
        url_final = f"{Url}genre/movie/list"

        response = requests.get(url_final, params=params)

        if response.status_code == 200:
            data = response.json()
            self.generos = data["genres"]  # Almacena los géneros en el atributo global
            return self.generos
        else:
            self.Messagen = f"Error al obtener los géneros: {response.status_code}"
            return  self.Messagen

    def getStoredGenres(self):
        """Método para acceder a los géneros almacenados."""
        return self.generos

    def getGenederSt(self, genere_id:int, total_movies:int):
        # Variables de almacenamiento y contador
        movies = []
        page = 1
    
        # URL base de la consulta
        url_final = f"{self.getUrlBase()}discover/movie"
    
        while len(movies) < total_movies:  # Mientras no alcances el limite de películas
            params = {
                "api_key": self.getKey(),
                "language": "es-ES",
                "with_genres": genere_id,
                "page": page
            }
            response = requests.get(url_final, params=params)
            
            if response.status_code == 200:
                data = response.json()
                movies.extend(data["results"])
                
                # Detener si llegamos a la ultima página
                if page >= data["total_pages"]:
                    break
    
                page += 1
            else:
                print(f"Error al obtener películas: {response.status_code}")
                break
        #creando un dataFrame con los datos necesarios de las peliculas
        dtMovies = pd.DataFrame(movies)[["id","title", "popularity", "vote_average", "vote_count", "genre_ids"]]
        
        # Retornar solo el número deseado de películas (en caso de exceder total_movies)
        return dtMovies.head(total_movies)
       
class GenderAnalysis(MoviesGenere):
    
    def __init__(self):
        self.movies_data = {}  # Inicializa un diccionario vacío

    #obtener las ids de las peliculas de un genero
    def Id_genders_movies(self, movies):
        moviesDict = movies
        ids_movies = [d["id"] for d in moviesDict]
        return ids_movies

    def GetMoviesEveryGender(self, generos, cantidad):
        # Lista para almacenar promedios por género
        calificaciones_por_genero = []
        cantidad_peliculas = []
        popularidad_por_genero = []
        
        # Iterar por cada genero
        for genero in generos:
            # Obtener el ID del género
            gender_id = genero['id']
            
            # Obtener las películas del género actual
            peliculas = super().getGenederSt(gender_id, cantidad)#esto es un dataFrame

            #obteniendo el promedio de las calificaciones
            promedio_calificaciones = peliculas["vote_average"].mean()
            # Agregar el promedio a la lista
            calificaciones_por_genero.append(promedio_calificaciones)

            #obteniendo el promedio de vistas
            promedio_popularidad = peliculas["popularity"].mean()
            #Agregar el promedio a la lista
            popularidad_por_genero.append(promedio_popularidad)

            #agregando la cantidad de peliculas analizadas
            cantidad_peliculas.append(cantidad)
    
        # Convertir el diccionario de géneros a un DataFrame
        dtGenders = pd.DataFrame(generos)
        
        # Verificar que las longitudes coincidan antes de asignar la columna
        if len(dtGenders) == len(calificaciones_por_genero):
            dtGenders["Media de Calificaciones"] = calificaciones_por_genero
        else:
            raise ValueError("Longitud desalineada entre géneros y calificaciones.")

        #visualizaciones por genero
        dtGenders["Media Visualizaciones"] = popularidad_por_genero

        #agregandole la cantidad de peliculas que se han tomado en cuenta para el promedio
        dtGenders["Cantidad de peliculas"] = cantidad_peliculas
        #retornando el diccionario
        return dtGenders

    #obtener la media de popularidad por genero de las peliculas de un genero
    def Id_genders_movies(self, movies):
        moviesDict = movies
        ids_movies = [d["id"] for d in moviesDict]
        return ids_movies




