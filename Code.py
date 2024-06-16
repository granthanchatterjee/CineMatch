import tkinter as tk
from tkinter import ttk, messagebox

class Movie:
    def __init__(self, title, genre, industry, celebrity, platform, platform_rent, total_time, watch_time):
        self.title = title
        self.genre = genre
        self.industry = industry
        self.celebrity = celebrity
        self.platform = platform
        self.platform_rent = platform_rent
        self.total_time = total_time
        self.watch_time = watch_time
        self.score = self.calculate_score()
        self.rating = self.scale_rating()

    def calculate_score(self):
        genre_scores = {'Action': 3, 'Drama': 1, 'Horror': 3, 'Comedy': 2, 'Romance': 2, 'Sci-Fi': 3, 'Adventure': 1, 'Mystery': 3, 'Fantasy': 1}
        industry_scores = {'Hollywood': 1, 'Indian': 3, 'Anime': 2, 'Indi': 1, 'Korean': -2}
        platform_scores = {'Netflix': 2, 'Prime': 1, 'Youtube': 2, 'Disney Plus Hotstar': 0, 'MX Player':0, 'Zee5': 1}

        score = 0
        score += genre_scores.get(self.genre, 0)
        score += industry_scores.get(self.industry, 0)
        score += 3 if self.celebrity else 0
        score += platform_scores.get(self.platform, 0)
        score += 3 if self.platform_rent == 0 else 0
        time_ratio = self.watch_time / self.total_time
        if time_ratio >= 0.9:
            score += 3
        elif time_ratio >= 0.8:
            score += 2
        elif time_ratio >= 0.7:
            score += 1
        else:
            score -= 3

        return score

    def scale_rating(self):
        min_score = -6
        max_score = 15
        scaled_rating = ((self.score - min_score) / (max_score - min_score)) * 5
        return round(scaled_rating, 2)

class CineMatch:
    def __init__(self):
        self.movies = []
        self.title_index = {}
        self.genre_index = {}

    def add_movie(self, movie):
        self.movies.append(movie)
        if movie.title not in self.title_index:
            self.title_index[movie.title] = []
        self.title_index[movie.title].append(len(self.movies) - 1)
        if movie.genre not in self.genre_index:
            self.genre_index[movie.genre] = []
        self.genre_index[movie.genre].append(len(self.movies) - 1)

    def search_movie_by_title(self, title):
        if title in self.title_index:
            return [self.movies[i] for i in self.title_index[title]]
        return []

    def search_movie_by_genre(self, genre):
        if genre in self.genre_index:
            return [self.movies[i] for i in self.genre_index[genre]]
        return []

    def delete_movie(self, title):
        if title in self.title_index:
            indices = self.title_index.pop(title)
            for i in sorted(indices, reverse=True):
                movie = self.movies.pop(i)
                self.genre_index[movie.genre].remove(i)
                if not self.genre_index[movie.genre]:
                    self.genre_index.pop(movie.genre)
            return True
        return False

    def quick_sort(self, movies):
        if len(movies) <= 1:
            return movies
        pivot = movies[len(movies) // 2].rating
        left = [x for x in movies if x.rating > pivot]
        middle = [x for x in movies if x.rating == pivot]
        right = [x for x in movies if x.rating < pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)

    def recommend_top_n_movies(self, n):
        sorted_movies = self.quick_sort(self.movies)
        return sorted_movies[:n]

class CineMatchApp:
    def __init__(self, root, cine_match):
        self.cine_match = cine_match
        self.root = root
        self.root.title("CineMatch Movie Recommendation System")
        self.root.configure(bg="black")
        self.root.geometry("800x600")

        style = ttk.Style()
        style.configure("TLabel", background="black", foreground="yellow", font=("Helvetica", 12))
        style.configure("TButton", background="yellow", foreground="black", font=("Helvetica", 12))
        style.configure("TCombobox", background="yellow", foreground="black", font=("Helvetica", 12))

        self.title_label = tk.Label(root, text="CineMatch", bg="black", fg="yellow", font=("Helvetica", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=20, sticky="n")

        self.separator = ttk.Separator(root, orient="horizontal")
        self.separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=20)

        self.input_frame = tk.Frame(root, bg="black")
        self.input_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nw")

        self.title_label_input = ttk.Label(self.input_frame, text="Title")
        self.title_entry = ttk.Entry(self.input_frame, font=("Helvetica", 12))

        self.genre_label = ttk.Label(self.input_frame, text="Genre")
        self.genre_combobox = ttk.Combobox(self.input_frame, values=["Action", "Drama", "Horror", "Comedy", "Romance", "Sci-Fi", "Adventure", "Mystery","Fantasy"], font=("Helvetica", 12))

        self.industry_label = ttk.Label(self.input_frame, text="Industry")
        self.industry_combobox = ttk.Combobox(self.input_frame, values=["Hollywood", "Indian", "Anime", "Indi", "Korean"], font=("Helvetica", 12))

        self.celebrity_label = ttk.Label(self.input_frame, text="Celebrity")
        self.celebrity_combobox = ttk.Combobox(self.input_frame, values=["Yes", "No"], font=("Helvetica", 12))

        self.platform_label = ttk.Label(self.input_frame, text="Platform")
        self.platform_combobox = ttk.Combobox(self.input_frame, values=["Netflix", "Prime", "Youtube", "Disney Plus Hotstar", "MX Player", "Zee5"], font=("Helvetica", 12))

        self.platform_rent_label = ttk.Label(self.input_frame, text="Platform Rent (INR)")
        self.platform_rent_entry = ttk.Entry(self.input_frame, font=("Helvetica", 12))

        self.total_time_label = ttk.Label(self.input_frame, text="Total Time (minutes)")
        self.total_time_entry = ttk.Entry(self.input_frame, font=("Helvetica", 12))

        self.watch_time_label = ttk.Label(self.input_frame, text="Watch Time (minutes)")
        self.watch_time_entry = ttk.Entry(self.input_frame, font=("Helvetica", 12))

        self.title_label_input.grid(row=0, column=0, pady=5, sticky="w")
        self.title_entry.grid(row=0, column=1, pady=5, sticky="w")
        self.genre_label.grid(row=1, column=0, pady=5, sticky="w")
        self.genre_combobox.grid(row=1, column=1, pady=5, sticky="w")
        self.industry_label.grid(row=2, column=0, pady=5, sticky="w")
        self.industry_combobox.grid(row=2, column=1, pady=5, sticky="w")
        self.celebrity_label.grid(row=3, column=0, pady=5, sticky="w")
        self.celebrity_combobox.grid(row=3, column=1, pady=5, sticky="w")
        self.platform_label.grid(row=4, column=0, pady=5, sticky="w")
        self.platform_combobox.grid(row=4, column=1, pady=5, sticky="w")
        self.platform_rent_label.grid(row=5, column=0, pady=5, sticky="w")
        self.platform_rent_entry.grid(row=5, column=1, pady=5, sticky="w")
        self.total_time_label.grid(row=6, column=0, pady=5, sticky="w")
        self.total_time_entry.grid(row=6, column=1, pady=5, sticky="w")
        self.watch_time_label.grid(row=7, column=0, pady=5, sticky="w")
        self.watch_time_entry.grid(row=7, column=1, pady=5, sticky="w")

        self.button_frame = tk.Frame(root, bg="black")
        self.button_frame.grid(row=2, column=1, padx=20, pady=20, sticky="ne")

        self.add_button = ttk.Button(self.button_frame, text="Add Movie", command=self.add_movie)
        self.recommend_button = ttk.Button(self.button_frame, text="Recommend Movies", command=self.recommend_movies)
        self.search_title_button = ttk.Button(self.button_frame, text="Search by Title", command=self.search_movie_by_title)
        self.search_genre_button = ttk.Button(self.button_frame, text="Search by Genre", command=self.search_movie_by_genre)
        self.delete_button = ttk.Button(self.button_frame, text="Delete Movie", command=self.delete_movie)

        self.add_button.grid(row=0, column=0, pady=10, sticky="e")
        self.recommend_button.grid(row=1, column=0, pady=10, sticky="e")
        self.search_title_button.grid(row=2, column=0, pady=10, sticky="e")
        self.search_genre_button.grid(row=3, column=0, pady=10, sticky="e")
        self.delete_button.grid(row=4, column=0, pady=10, sticky="e")

        self.movie_listbox = tk.Listbox(root, width=80, height=20, bg="black", fg="yellow", font=("Helvetica", 12))
        self.movie_listbox.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

    def add_movie(self):
        try:
            title = self.title_entry.get()
            genre = self.genre_combobox.get()
            industry = self.industry_combobox.get()
            celebrity = self.celebrity_combobox.get() == "Yes"
            platform = self.platform_combobox.get()
            platform_rent = float(self.platform_rent_entry.get())
            total_time = float(self.total_time_entry.get())
            watch_time = float(self.watch_time_entry.get())

            movie = Movie(title, genre, industry, celebrity, platform, platform_rent, total_time, watch_time)
            self.cine_match.add_movie(movie)
            self.update_movie_listbox()
            messagebox.showinfo("Success", "Movie added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_movie_listbox(self):
        self.movie_listbox.delete(0, tk.END)
        for movie in self.cine_match.movies:
            self.movie_listbox.insert(tk.END, f"{movie.title} - {movie.genre} - Rating: {movie.rating}")

    def recommend_movies(self):
        top_movies = self.cine_match.recommend_top_n_movies(5)
        if top_movies:
            recommendations = "\n".join([f"{movie.title} (Rating: {movie.rating})" for movie in top_movies])
            messagebox.showinfo("Top Movies", recommendations)
        else:
            messagebox.showinfo("No Movies", "No movies to recommend.")

    def search_movie_by_title(self):
        title = self.title_entry.get()
        movies = self.cine_match.search_movie_by_title(title)
        if movies:
            search_results = "\n".join([f"{movie.title} - {movie.genre} - Rating: {movie.rating}" for movie in movies])
            messagebox.showinfo("Search Results", search_results)
        else:
            messagebox.showinfo("No Movies", f"No movies found with title: {title}")

    def search_movie_by_genre(self):
        genre = self.genre_combobox.get()
        movies = self.cine_match.search_movie_by_genre(genre)
        if movies:
            search_results = "\n".join([f"{movie.title} - {movie.genre} - Rating: {movie.rating}" for movie in movies])
            messagebox.showinfo("Search Results", search_results)
        else:
            messagebox.showinfo("No Movies", f"No movies found with genre: {genre}")

    def delete_movie(self):
        title = self.title_entry.get()
        if self.cine_match.delete_movie(title):
            self.update_movie_listbox()
            messagebox.showinfo("Success", f"Movie '{title}' deleted successfully!")
        else:
            messagebox.showinfo("Error", f"No movie found with title: {title}")

cine_match = CineMatch()
root = tk.Tk()
app = CineMatchApp(root, cine_match)
root.mainloop()