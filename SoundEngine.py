import pygame, copy
from random import randint

pygame.mixer.set_num_channels(64)

win_jingle = pygame.mixer.Sound("Sounds/win.wav")

loss_jingle = pygame.mixer.Sound("Sounds/loss.wav")

theme = pygame.mixer.music.load("Sounds/theme.wav")

laser_sound = pygame.mixer.Sound("Sounds/laser.wav")

spaceship_hitsound = pygame.mixer.Sound("Sounds/hit.wav")

mistery_hitsound = pygame.mixer.Sound("Sounds/mistery.wav")

silence = pygame.mixer.Sound("Sounds/silence.wav")

drums = [[pygame.mixer.Sound("Sounds/drums_11.wav"), pygame.mixer.Sound("Sounds/drums_12.wav"), silence],
        [pygame.mixer.Sound("Sounds/drums_21.wav"), pygame.mixer.Sound("Sounds/drums_22.wav"), silence],
        [pygame.mixer.Sound("Sounds/drums_31.wav"), pygame.mixer.Sound("Sounds/drums_32.wav"), silence],
        [pygame.mixer.Sound("Sounds/drums_41.wav"), pygame.mixer.Sound("Sounds/drums_42.wav"), silence],]

hihat = [[pygame.mixer.Sound("Sounds/hihat_11.wav"), pygame.mixer.Sound("Sounds/hihat_12.wav"), silence],
         [pygame.mixer.Sound("Sounds/hihat_21.wav"), pygame.mixer.Sound("Sounds/hihat_22.wav"), silence],
         [pygame.mixer.Sound("Sounds/hihat_31.wav"), pygame.mixer.Sound("Sounds/hihat_32.wav"), silence],
         [pygame.mixer.Sound("Sounds/hihat_41.wav"), pygame.mixer.Sound("Sounds/hihat_42.wav"), silence],]

voice2 = [[pygame.mixer.Sound("Sounds/voice2_11.wav"), pygame.mixer.Sound("Sounds/voice2_12.wav"), silence],
          [pygame.mixer.Sound("Sounds/voice2_21.wav"), pygame.mixer.Sound("Sounds/voice2_22.wav"), silence],
          [pygame.mixer.Sound("Sounds/voice2_31.wav"), pygame.mixer.Sound("Sounds/voice2_32.wav"), silence],
          [pygame.mixer.Sound("Sounds/voice2_41.wav"), pygame.mixer.Sound("Sounds/voice2_42.wav"), silence],]

voice1 = [[pygame.mixer.Sound("Sounds/voice1_11.wav"), pygame.mixer.Sound("Sounds/voice1_12.wav"), silence],
          [pygame.mixer.Sound("Sounds/voice1_21.wav"), pygame.mixer.Sound("Sounds/voice1_22.wav"), silence],
          [pygame.mixer.Sound("Sounds/voice1_31.wav"), pygame.mixer.Sound("Sounds/voice1_32.wav"), silence],
          [pygame.mixer.Sound("Sounds/voice1_41.wav"), pygame.mixer.Sound("Sounds/voice1_42.wav"), silence],]

bass =   [[pygame.mixer.Sound("Sounds/bass_11.wav"), pygame.mixer.Sound("Sounds/bass_12.wav"), silence],
          [pygame.mixer.Sound("Sounds/bass_21.wav"), pygame.mixer.Sound("Sounds/bass_22.wav"), silence],
          [pygame.mixer.Sound("Sounds/bass_31.wav"), pygame.mixer.Sound("Sounds/bass_32.wav"), silence],
          [pygame.mixer.Sound("Sounds/bass_41.wav"), pygame.mixer.Sound("Sounds/bass_42.wav"), silence],]

# first block digit: beat number (1->4)
# second block digit: instrument (0:basso -> 4:drum)
INITIAL_BLOCK_STATUS = {
    10:{"status":0, "active":False},
    20:{"status":0, "active":False},
    30:{"status":0, "active":False},
    40:{"status":0, "active":False},
    11:{"status":0, "active":False},
    21:{"status":0, "active":False},
    31:{"status":0, "active":False},
    41:{"status":0, "active":False},
    12:{"status":0, "active":False},
    22:{"status":0, "active":False},
    32:{"status":0, "active":False},
    42:{"status":0, "active":False},
    13:{"status":0, "active":False},
    23:{"status":0, "active":False},
    33:{"status":0, "active":False},
    43:{"status":0, "active":False},
    14:{"status":0, "active":False},
    24:{"status":0, "active":False},
    34:{"status":0, "active":False},
    44:{"status":0, "active":False},
}

blocks_status = copy.deepcopy(INITIAL_BLOCK_STATUS)

def playbeat(beat):
    for block, status in blocks_status.items():
        if str(block)[0] == str(beat):
            if status["active"]:
                # gets active blocks at the current beat
                if str(block)[1] == "0":    #bass
                    pygame.mixer.find_channel().play(bass[beat-1][status["status"]])

                elif str(block)[1] == "1":  #voice1
                    pygame.mixer.find_channel().play(voice1[beat-1][status["status"]])

                elif str(block)[1] == "2":  #voice2
                    pygame.mixer.find_channel().play(voice2[beat-1][status["status"]])

                elif str(block)[1] == "3":  #hihat
                    pygame.mixer.find_channel().play(hihat[beat-1][status["status"]])
                
                elif str(block)[1] == "4":  #drums
                    pygame.mixer.find_channel().play(drums[beat-1][status["status"]])

def alienkilled(block, status):
    if not blocks_status[block]["active"]:
        blocks_status[block]["active"] = True
        blocks_status[block]["status"] = status

def spaceship_hit():
    pygame.mixer.find_channel().play(spaceship_hitsound)

def laser():
    pygame.mixer.find_channel().play(laser_sound)

def misteryscrumble():
    pygame.mixer.find_channel().play(mistery_hitsound)
    for condition in blocks_status.values():
        condition["status"] = randint(0, 2)

def blocks_reset():
    global blocks_status, INITIAL_BLOCK_STATUS
    blocks_status = copy.deepcopy(INITIAL_BLOCK_STATUS)

def play_win():
    pygame.mixer.find_channel().play(win_jingle)

def play_loss():
    pygame.mixer.find_channel().play(loss_jingle)

def theme_in(fade_time):
    pygame.mixer.music.play(loops=-1, fade_ms=fade_time)

def theme_out():
    pygame.mixer.music.fadeout(1000)

def prova():
    test_sound = pygame.mixer.Sound(drums[0][0])
    test_sound.play()