## Opis

Ten skrypt w języku Python rekomenduje film losowo wybranemu użytkownikowi na podstawie filtrowania kolaboratywnego. Wykorzystuje zestaw danych zawierający oceny użytkowników dla różnych filmów.

## Funkcje

1. `userIdToIndex(userSet, userId=None)`: Mapuje identyfikatory użytkowników na indeksy w zbiorze.
2. `movieIdToIndex(movieSet, movieId=None)`: Mapuje identyfikatory filmów na indeksy w zbiorze.
3. `loadData()`: Wczytuje zestaw danych z ocenami, konstruuje macierz ocen i zwraca unikalne zbiory użytkowników i filmów.
4. `findNearestUsers(targetUserId, ratingsMatrix, numNeighbors, uniqueUsers)`: Znajduje najbliższych użytkowników do wybranego użytkownika na podstawie podobieństwa ocen.
5. `suggestMovie(targetUserId, ratingsMatrix, neighbors, userSimilarity, uniqueUsers, uniqueMovies)`: Sugeruje film wybranemu użytkownikowi na podstawie ocen najbliższych sąsiadów.

## Użycie

1. Wczytaj dane za pomocą funkcji `loadData()`.
2. Wybierz losowy identyfikator użytkownika.
3. Znajdź najbliższych użytkowników wybranego użytkownika.
4. Zasugeruj film wybranemu użytkownikowi na podstawie zachowania najbliższych sąsiadów.
