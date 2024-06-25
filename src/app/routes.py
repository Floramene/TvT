from flask import Blueprint, render_template, request, redirect, url_for, session
from .tmdb import TMDBClient

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'use_public_key' in request.form:
            public_keys = [
                request.form['public_api_key_1'],
                request.form['public_api_key_2']
            ]
            for api_key in public_keys:
                if TMDBClient.verify_api_key(api_key):
                    session['api_key'] = api_key
                    return redirect(url_for('main.media_list', media_type='movie'))
            return render_template('index.html', error='Both public API keys failed.')
        else:
            api_key = request.form['api_key']
            if TMDBClient.verify_api_key(api_key):
                session['api_key'] = api_key
                return redirect(url_for('main.media_list', media_type='movie'))
            return render_template('index.html', error='Invalid API key')
    return render_template('index.html')

@main.route('/<media_type>s')
def media_list(media_type):
    if media_type not in ['movie', 'show']:
        return redirect(url_for('main.index'))
    return render_media_list(media_type)

def render_media_list(media_type):
    api_key = session.get('api_key', None)
    if not api_key:
        return redirect(url_for('main.index'))

    tmdb_client = TMDBClient(api_key)
    fetch_type = "movie" if media_type == "movie" else "tv"
    search_query = request.args.get('search')
    genre_id = request.args.get('genre')
    titles = tmdb_client.fetch_media_list(fetch_type, search_query, genre_id)
    genres = tmdb_client.fetch_genres(fetch_type)

    return render_template(
        'title_list.html',
        titles=titles,
        genres=genres,
        media_type=media_type
    )

@main.route('/<string:content_type>/<int:title_id>')
def title_detail(content_type, title_id):
    api_key = session.get('api_key', None)
    if not api_key:
        return redirect(url_for('main.index'))

    tmdb_client = TMDBClient(api_key)
    fetch_type = "movie" if content_type == "movie" else "tv"
    title = tmdb_client.fetch_data(fetch_type, f'{title_id}')
    return render_template('title_details.html', media_type=content_type, title=title)

@main.route('/show/<int:show_id>/<int:season_number>')
def season_detail(show_id, season_number):
    api_key = session.get('api_key', None)
    if not api_key:
        return redirect(url_for('main.index'))

    tmdb_client = TMDBClient(api_key)
    season = tmdb_client.fetch_data(f'tv/{show_id}/season', f'{season_number}')
    return render_template('season_detail.html', series_id=show_id, season=season)

@main.route('/<string:content_type>/watch/<int:content_id>', defaults={'season_number': None, 'episode_number': None})
@main.route('/<string:content_type>/watch/<int:content_id>/<int:season_number>/<int:episode_number>')
def title_watch(content_type, content_id, season_number, episode_number):
    api_key = session.get('api_key', None)
    if not api_key:
        return redirect(url_for('main.index'))

    tmdb_client = TMDBClient(api_key)
    if content_type == 'movie':
        content = tmdb_client.fetch_data('movie', f'{content_id}')
        title = content['title']
    elif content_type == 'show':
        content_type = 'tv'
        if season_number and episode_number:
            content = tmdb_client.fetch_data(f'tv/{content_id}/season', f'{season_number}')
            episode = next((ep for ep in content['episodes'] if ep['episode_number'] == episode_number), None)
            title = f"S{season_number} E{episode_number} - {episode['name']}" if episode else "Episode"
        else:
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.index'))

    return render_template('title_watch.html', content=content, content_type=content_type, title=title, season_number=season_number, episode_number=episode_number, content_id=content_id)

@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
