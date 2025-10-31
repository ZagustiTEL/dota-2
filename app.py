from flask import Flask, render_template

app = Flask(__name__)

# Данные о героях
heroes = [
    {
        'name': 'Anti-Mage',
        'role': 'Carry',
        'attribute': 'Agility',
        'description': 'Могущий воин, охотник на магов'
    },
    {
        'name': 'Crystal Maiden',
        'role': 'Support',
        'attribute': 'Intelligence',
        'description': 'Волшебница, контролирующая лед и холод'
    },
    {
        'name': 'Axe',
        'role': 'Initiator',
        'attribute': 'Strength',
        'description': 'Бесстрашный воин с огромным топором'
    },
    {
        'name': 'Invoker',
        'role': 'Carry',
        'attribute': 'Intelligence',
        'description': 'Маг, владеющий множеством заклинаний'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heroes')
def heroes_page():
    return render_template('heroes.html', heroes=heroes)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)