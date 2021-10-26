from table2ascii import table2ascii as t2a, PresetStyle, Alignment
from Player import Player

class scoreboardshow(object):
    
    def show(cur):
        cur.execute( "select Name, TotalPoints from Players" )
        result = cur.fetchall()
        result = [[str(x) for x in y] for y in result]
        result.sort(key=lambda k: k[1], reverse=True) #разобраться в лямбде
        output = t2a(
            header = ["Игрок", "Очки"],
            body = result,
            first_col_heading=True,
            alignments = [Alignment.LEFT] + [Alignment.RIGHT],
            style=PresetStyle.thin_compact_rounded
        )
        return output

    def show_in_game_table(list):

        playerstable = []
        for x in list:
            playerstable.append([x.name, x.score])

        playerstable = [[str(x) for x in y] for y in playerstable]
        playerstable.sort(key=lambda k: k[1], reverse=True)
        output = t2a(
            header = ["Игрок", "Очки"],
            body = playerstable,
            first_col_heading=True,
            alignments = [Alignment.LEFT] + [Alignment.RIGHT],
            style=PresetStyle.thick
        )
        return output




