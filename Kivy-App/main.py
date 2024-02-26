from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from kivy.storage.jsonstore import JsonStore
import requests


class MovieListItem(TwoLineListItem):
    def __init__(self, movie_id, plot, **kwargs):
        super(MovieListItem, self).__init__(**kwargs)
        self.movie_id = movie_id
        self.plot = plot


class HomeScreen(Screen):
    def on_enter(self):
        # Fetch the movie list from your API and populate the screen
        movie_list = self.get_movie_list()

        # Get the reference to the movie_list ScrollView
        movie_list_scrollview = self.ids.movie_list_scrollview

        # Clear existing widgets
        movie_list_scrollview.clear_widgets()

        # Populate the movie_list ScrollView with ThreeLineListItem widgets
        for movie in movie_list:
            print(movie)
            item = MovieListItem(movie_id=movie['id'], text=movie['title'], plot=movie['plot'], secondary_text=f"Year: {movie['year']}")
            item.bind(on_release=self.on_movie_click)
            movie_list_scrollview.add_widget(item)

    def on_movie_click(self, instance):
        # Navigate to the Rating screen with movie details
        app = MDApp.get_running_app()
        app.movie_details = {
            'id': instance.movie_id,
            'text': instance.text,
            'year': instance.secondary_text.split(":")[1].strip(),
            'plot': instance.plot,
        }
        app.root.transition.direction = 'left'
        app.root.current = 'rating'

    def get_movie_list(self):
        url = "http://127.0.0.1:8000/api/movies/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return ["Error fetching movie list"]

    def on_login_pre(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'left'
        app.root.current = 'login'


class RatingScreen(Screen):
    def __init__(self, **kwargs):
        super(RatingScreen, self).__init__(**kwargs)

    def update_rating_label(self):
        # Update the label to display the current rating value
        self.ids.rating_label.text = f"Current Rating: {self.ids.rating_slider.value}"

    def on_pre_enter(self):
        # Populate the Rating screen with movie details
        app = MDApp.get_running_app()
        movie_details = app.movie_details
        self.ids.movie_title.text = movie_details['text']
        self.ids.movie_info.text = f"Year: {movie_details['year']}"

    def submit_rating(self):
        store = JsonStore('user_data.json')

        if store.exists('user_token'):
            user_token = store.get('user_token')
            app = MDApp.get_running_app()
            rating = self.ids.rating_slider.value
            movie_id = app.movie_details['id']
            review_text = self.ids.review_input.text
            review_data = {
                'movie': movie_id,
                'value': rating,
                'review': review_text
            }
            # You can now send these values to your API for submission
            # Replace the following line with your actual API request logic
            if user_token:
                url = "http://127.0.0.1:8000/api/reviews/"
                token = user_token['token']
                header_info = {'Authorization': f'Token {token}'}
                requests.post(url, headers=header_info, data=review_data)

                # Reset the input fields after submission
                self.ids.rating_slider.value = 5  # Reset the slider to the initial value
                self.ids.review_input.text = ''

                # Optionally, you can update the rating label after submission
                self.update_rating_label()

    def on_pre_leave(self):
        # Reset the input fields before leaving the RatingScreen
        self.ids.rating_slider.value = 5
        self.ids.review_input.text = ''

        # Optionally, update the rating label
        self.update_rating_label()

        # Navigate back to the HomeScreen
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'home'


class LoginScreen(Screen):
    STORE_NAME = 'user_data'

    def login(self):
        # Get the username and password from TextInput widgets
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        url = "http://127.0.0.1:8000/api/login-auth-token/"
        data = {'username': username, 'password': password}
        response = requests.post(url, data=data)
        store = JsonStore(f'{self.STORE_NAME}.json')
        if response.status_code == 200:
            user_token = response.json()['token']
            store.put('user_token', token=user_token)
        else:
            return ["Error fetching movie list"]

    def on_pre_leave(self):
        # Reset the input fields and login result label before leaving the LoginScreen
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''
        self.ids.login_result_label.text = ''

        # Optionally, you can update the screen manager transition direction
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'home'


class MovieRatingApp(MDApp):
    movie_details = {}

    def build(self):
        # Load the KV file
        Builder.load_file('main.kv')

        # Create a ScreenManager and add the screens
        screen_manager = ScreenManager()
        screen_manager.add_widget(HomeScreen(name='home'))
        screen_manager.add_widget(RatingScreen(name='rating'))
        screen_manager.add_widget(LoginScreen(name='login'))

        return screen_manager


if __name__ == '__main__':
    MovieRatingApp().run()
