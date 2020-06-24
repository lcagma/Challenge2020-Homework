import pygame as pg
import time
from EventManager import *
from Model import GameEngine
import Const


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.background.fill(Const.BACKGROUND_COLOR)

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pass

    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to start ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center = text_center))
        
        pg.display.flip()

    def render_play(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        
        # draw players
        for player in self.model.players:
            center = list(map(int, player.position))
            pg.draw.circle(self.screen, Const.PLAYER_COLOR[player.player_id], center, Const.PLAYER_RADIUS)

        #timeleft
        font = pg.font.Font(None, 36)
        change_time_surface = font.render(f"change time left: {self.model.changetime / Const.FPS:.2f}", 1, pg.Color('white'))
        change_time_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 20)
        self.screen.blit(change_time_surface, change_time_surface.get_rect(center = change_time_pos))

        time_left_surface = font.render(f"total time left: {self.model.timeleft / Const.FPS:.2f}", 1, pg.Color('white'))
        time_left_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] * 2 / 20)
        self.screen.blit(time_left_surface, time_left_surface.get_rect(center = time_left_pos))

        pause_surface = font.render(f"pause: press p", 1, pg.Color('white'))
        pause_pos = (Const.ARENA_SIZE[0] * 5 / 6, Const.ARENA_SIZE[1] / 20)
        self.screen.blit(pause_surface, pause_surface.get_rect(center = pause_pos))

        
        score_surface = font.render(f"player[0] score: {self.model.players[0].score :d}    player[1] score: {self.model.players[1].score :d}", 1, pg.Color('white'))
        score_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] * 3 / 20)
        self.screen.blit(score_surface, score_surface.get_rect(center = score_pos))
        pg.display.flip()        
    def render_stop(self):
        # draw players
        for player in self.model.players:
            center = list(map(int, player.position))
            pg.draw.circle(self.screen, Const.PLAYER_COLOR[player.player_id], center, Const.PLAYER_RADIUS)
        font = pg.font.Font(None, 36)
        resume_surface = font.render(f"resume: press o", 1, pg.Color('white'))
        resume_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(resume_surface, resume_surface.get_rect(center = resume_pos))
        pg.display.flip()
        
    def render_endgame(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        font = pg.font.Font(None, 36)
        score_surface = font.render(f"player[0] score: {self.model.players[0].score :d}    player[1] score: {self.model.players[1].score :d}", 1, pg.Color('white'))
        score_pos = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(score_surface, score_surface.get_rect(center = score_pos))
        pg.display.flip()
