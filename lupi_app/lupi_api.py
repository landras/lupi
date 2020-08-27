from lupi_app.lupi import Lupi


def start():
    (data, http_status) = Lupi.start_new_round()
    return data, http_status


def stop(round_id):
    return Lupi.stop_round(round_id)


def vote(vote):
    name = vote.get("name")
    number = vote.get("number")

    return Lupi.insert_vote(name, number)


def get_result(round_id):
    return Lupi.get_result(round_id)


def get_rounds():
    return Lupi.get_rounds()


def get_stat(round_id):
    return Lupi.get_stat(round_id)
