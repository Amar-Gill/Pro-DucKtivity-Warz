from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import peewee as pw
from config import Config
from models.user import User
from models.game import Game
from models.habit import Habit
from models.log_habit import LogHabit




games_blueprint = Blueprint('games',
                            __name__,
                            template_folder='templates')



#Dont forget to change game round id!!!!
@games_blueprint.route('/<username>/<game_id>', methods=["GET"])
def show(username, game_id):

    game = Game.get_or_none(Game.id == game_id)

    #Player 1
    user = User.get_or_none(User.username == username)    

    #Set up habit info
    user_habits = Habit.select().where((Habit.game_id == game_id) & (Habit.user_id == user.id))
    length_habit_list = len(user_habits)

    #progress bars

    progress = []
    user_more_to_go = []

    for habit in user_habits:
        approved_logs = LogHabit.select().where((LogHabit.sender_id == user.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == 2))        
        logged_habits = len(approved_logs)
        percentage = logged_habits / habit.frequency * 100
        progress.append(percentage)
        leftover = habit.frequency - logged_habits
        user_more_to_go.append(leftover)

    print(user_more_to_go)
    rounded_progress = [round(freq, 0) for freq in progress]


    #Player 2

    player_2 = User.get_or_none(User.id == game.player_2_id)
    player_2_username = player_2.username

    player2_habits = Habit.select().where((Habit.game_id == game_id) & (Habit.user_id == player_2.id))
    p2_habit_length = len(player2_habits)

    #Progress bars

    p2_progress = []

    for habit in player2_habits:
        approved_logs = LogHabit.select().where((LogHabit.sender_id == player_2.id) & (LogHabit.habit_id == habit.id) & (LogHabit.approved == True) & (LogHabit.game_round_id == 2))        
        logged_habits = len(approved_logs)
        percentage = logged_habits / habit.frequency * 100
        p2_progress.append(percentage)
    
    rounded_p2_progress = [round(freq, 0) for freq in p2_progress]

    return render_template('games/show.html', 
                            username = user.username, 
                            user_habits = user_habits, 
                            length_habit_list=length_habit_list, 
                            rounded_progress = rounded_progress, 
                            player_2_username = player_2_username,
                            player2_habits = player2_habits,
                            p2_habit_length = p2_habit_length,
                            rounded_p2_progress = rounded_p2_progress,
                            user_more_to_go = user_more_to_go,
                            game_id = game.id)





