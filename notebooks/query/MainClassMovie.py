import requests

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

