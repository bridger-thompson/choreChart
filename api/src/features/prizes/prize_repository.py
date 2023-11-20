from fastapi import HTTPException
from src.models.child import Child
from src.models.prize import Prize
from src.services.helper import run_sql


def get_parents_prizes(parent_id: int):
    sql = """
        SELECT * 
        FROM prize
        WHERE parent_id = %(parent_id)s
    """
    params = {"parent_id": parent_id}
    return run_sql(sql, params, output_class=Prize)


def get_parents_children_with_prize(prize_id: int, parent_id: int):
    sql = """
        SELECT c.*
        FROM child c
        INNER JOIN child_prize cp
            ON (c.id = cp.child_id)
        WHERE c.parent_id = %(parent_id)s
        AND cp.prize_id = %(prize_id)s
    """
    params = {"prize_id": prize_id, "parent_id": parent_id}
    return run_sql(sql, params, output_class=Child)


def add_prize(prize: Prize, parent_id: int):
    sql = """
        INSERT INTO prize (name, description, cost, image_filename, url, parent_id)
        VALUES (%(name)s, %(description)s, %(cost)s, %(image)s, %(url)s, %(parent_id)s)
        RETURNING *
    """
    params = {
        "name": prize.name,
        "description": prize.description,
        "cost": prize.cost,
        "image": prize.image_filename,
        "url": prize.url,
        "parent_id": parent_id,
    }
    return run_sql(sql, params, output_class=Prize)[0]


def update_prize(prize: Prize):
    sql = """
        UPDATE prize
        SET name = %(name)s,
            description = %(description)s,
            cost = %(cost)s,
            image_filename = %(image)s,
            url = %(url)s,
            active = %(active)s
        WHERE id = %(id)s
    """
    params = {
        "name": prize.name,
        "description": prize.description,
        "cost": prize.cost,
        "image": prize.image_filename,
        "url": prize.url,
        "active": prize.active,
        "id": prize.id,
    }
    run_sql(sql, params)


def delete_prize(id: int):
    sql = """
        DELETE FROM prize
        WHERE id = %(id)s
    """
    params = {"id": id}
    run_sql(sql, params)


def assign_prize_to_child(prize_id: int, child_id: int):
    sql = """
        INSERT INTO child_prize (child_id, prize_id)
        VALUES (%(child_id)s, %(prize_id)s)
    """
    params = {"child_id": child_id, "prize_id": prize_id}
    run_sql(sql, params)


def unassign_prize(prize_id: int):
    sql = """
        DELETE FROM child_prize
        WHERE prize_id = %(prize_id)s
    """
    params = {"prize_id": prize_id}
    run_sql(sql, params)


def get_childs_prizes(child_id: int):
    sql = """
        SELECT p.*
        FROM child_prize cp
        INNER JOIN prize p
            ON (p.id = cp.prize_id)
        WHERE cp.child_id = %(child_id)s
        AND p.active = true
    """
    params = {"child_id": child_id}
    return run_sql(sql, params, output_class=Prize)


def purchase_prize(child_prize_id: int):
    sql = """
        INSERT INTO purchased_prizes (child_prize_id)
        VALUES (%(id)s)
    """
    params = {"id": child_prize_id}
    run_sql(sql, params)


def get_prize(id: int):
    sql = """
        SELECT *
        FROM prize p
        WHERE p.id = %(id)s
    """
    params = {"id": id}
    return run_sql(sql, params, output_class=Prize)[0]


def get_child_prize_id(child_id: int, prize_id: int):
    sql = """
        SELECT id
        FROM child_prize
        WHERE child_id = %(child_id)s
        AND prize_id = %(prize_id)s
    """
    params = {
        "child_id": child_id,
        "prize_id": prize_id,
    }
    results = run_sql(sql, params)
    if results:
        return results[0][0]
    print(f"Unable to find child prize. Child: {child_id}, Prize: {prize_id}")
    raise HTTPException(status_code=400, detail="Unable to find child prize")
