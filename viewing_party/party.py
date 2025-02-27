# ------------- WAVE 1 --------------------

def create_movie(title, genre, rating):
    if not bool(title) or not bool(genre) or not bool(rating):
        return None

    new_movie = {"title": title, "genre": genre, "rating": rating}
    return new_movie


def add_to_watched(user_data, movie):
    if not bool(movie):
        return user_data
    user_data["watched"].append(movie)
    return user_data


def add_to_watchlist(user_data, movie):
    if not bool(movie):
        return user_data
    user_data["watchlist"].append(movie)
    return user_data


def watch_movie(user_data, title):
    for movie in user_data["watchlist"]:
        if movie["title"] == title:
            add_to_watched(user_data, movie)
            user_data["watchlist"].remove(movie)
            return user_data
    return user_data

# -----------------------------------------
# ------------- WAVE 2 --------------------
# -----------------------------------------


def get_watched_avg_rating(user_data):
    watched_len = len(user_data["watched"])
    if watched_len == 0:
        return 0.0

    rating_sum = 0
    for movie in user_data["watched"]:
        rating_sum += movie["rating"]

    avg_rating = rating_sum / watched_len
    return avg_rating


def get_most_watched_genre(user_data):
    if len(user_data["watched"]) == 0:
        return None

    watched_genres = {}
    for movie in user_data["watched"]:
        watched_genres[movie["genre"]] = watched_genres.get(movie["genre"], 0) + 1

    popular_genre = max(watched_genres, key=watched_genres.get)
    return popular_genre

# -----------------------------------------
# ------------- WAVE 3 --------------------
# -----------------------------------------


def get_unique_watched(user_data):
    watched_movies_list = user_data["watched"]
    friends_watched_movies_list = get_friends_watched_movies(user_data)
    return [movie for movie in watched_movies_list if movie not in friends_watched_movies_list]


def get_friends_unique_watched(user_data):
    watched_movies_list = user_data["watched"]
    friends_watched_movies_list = get_friends_watched_movies(user_data)
    remove_movie_duplicates(friends_watched_movies_list)

    friends_unique_list = [movie for movie in friends_watched_movies_list if movie not in watched_movies_list]
    return friends_unique_list


def get_friends_watched_movies(user_data):
    friends_watched_movies_list = []

    for friends_watched_movies in user_data["friends"]:
        friends_watched_movies_list.append(friends_watched_movies["watched"])

    friends_watched_movies_list = sum(friends_watched_movies_list, [])
    return friends_watched_movies_list


def remove_movie_duplicates(friends_watched_movies_list):
    friends_watched_movie_titles = {}
    for movie in friends_watched_movies_list:
        friends_watched_movie_titles[movie["title"]] = friends_watched_movie_titles.get(movie["title"], 0) + 1
        if friends_watched_movie_titles[movie["title"]] > 1:
            friends_watched_movies_list.remove(movie)
            friends_watched_movie_titles[movie["title"]] = friends_watched_movie_titles[movie["title"]] - 1
    return friends_watched_movies_list


# -----------------------------------------
# ------------- WAVE 4 --------------------
# -----------------------------------------


def get_available_recs(user_data):
    friends_available_recs = get_friends_unique_watched(user_data)
    available_recs = []
    for movie in friends_available_recs:
        if movie["host"] in user_data["subscriptions"]:
            available_recs.append(movie)
    return available_recs

# -----------------------------------------
# ------------- WAVE 5 --------------------
# -----------------------------------------


def get_new_rec_by_genre(user_data):
    friends_available_recs = get_friends_unique_watched(user_data)
    if len(user_data["watched"]) == 0 or len(friends_available_recs) == 0:
        return []

    popular_genre = get_most_watched_genre(user_data)
    recs_by_genre = []
    for movie in friends_available_recs:
        if movie["genre"] == popular_genre:
            recs_by_genre.append(movie)
    
    return recs_by_genre


def get_rec_from_favorites(user_data):
    if len(user_data["watched"]) == 0:
        return []

    if len(user_data["friends"]) == 0:
        return user_data["watched"]

    unique_watched = get_unique_watched(user_data)
    rec_from_favorites = []
    for movie in unique_watched:
        if movie in user_data["favorites"]:
            rec_from_favorites.append(movie)
    return rec_from_favorites
