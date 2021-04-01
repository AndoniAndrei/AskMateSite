import controller
import database_common


@database_common.connection_handler
def get_all_data(cursor, table, order_by, direction):
    cursor.execute(
        f"""
     SELECT * FROM {table}
     ORDER BY {order_by} {direction}
     """)
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_data_by_question_id(cursor, table, data_id):
    column = "id"
    if table == "answer":
        column = "question_id"
    if table == "comment":
        column = "question_id"
    if table == "question_tag":
        column = "question_id"
    cursor.execute(
        f"""
    SELECT * FROM {table}
    WHERE {column} = %(id)s;
    """,
        {"id": data_id},
    )
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_comments(cursor):
    cursor.execute(f"""
    SELECT * FROM comment
    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_data_by_answer_id(cursor, table, data_id):
    column = "id"
    if table == "comment":
        column = "answer_id"
    cursor.execute(
        f"""
    SELECT * FROM {table}
    WHERE {column} = %(id)s;
    """,
        {"id": data_id},
    )
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_answer_by_answer_id(cursor, table, answer_id):
    column = "id"
    cursor.execute(
        f"""
    SELECT * FROM {table}
    WHERE {column} = %(id)s;
    """,
        {"id": answer_id},
    )
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def add_new_question(cursor, title, message, image, username):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO question(submission_time, view_number, vote_number, title, message, image, username)
    VALUES (%(submission_time)s,0, 0, %(title)s, %(message)s, %(image)s, %(username)s)
    """,
        {
            "submission_time": submission_time,
            "title": title,
            "message": message,
            "image": image,
            "username": username
        },
    )


@database_common.connection_handler
def add_new_answer(cursor, message, image, question_id, username):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO answer(submission_time, vote_number, question_id, message, image, username)
    VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s, %(username)s) """,
        {
            "submission_time": submission_time,
            "message": message,
            "image": image,
            "question_id": question_id,
            "username": username
        },
    )


@database_common.connection_handler
def delete_data(cursor, data_id, table):
    column = "id"
    cursor.execute(
        f"""
    DELETE FROM {table} WHERE {column}=%(id)s
    """,
        {"id": data_id},
    )


@database_common.connection_handler
def edit_question(cursor, table, item_id, title, message, image, username):
    column = "id"
    cursor.execute(
        f"""
    UPDATE {table}
    SET title = %(title)s, message = %(message)s, image = %(image)s
    WHERE {column} = %(id)s 
    """,
        {"message": message, "title": title, "image": image, "id": item_id, "username": username},
    )


@database_common.connection_handler
def edit_answer(cursor, answer_id, message, username):
    cursor.execute(f"""
    UPDATE answer SET message = %(message)s
    WHERE id = %(id)s
        """, {"id": answer_id, "message": message, "username": username})


@database_common.connection_handler
def edit_comment(cursor, comment_id, message, username):
    cursor.execute(f"""
        UPDATE comment SET message = %(message)s
        WHERE id = %(id)s
            """, {"id": comment_id, "message": message, "username": username})





@database_common.connection_handler
def add_comment_question(cursor, question_id, message, username):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO comment(submission_time, question_id, message, username)
    VALUES (%(submission_time)s, %(question_id)s, %(message)s, %(username)s)""",
        {
            "submission_time": submission_time,
            "message": message,
            "question_id": question_id,
            "username": username
        },
    )


@database_common.connection_handler
def add_comment_answer(cursor, answer_id, message, username):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO comment(answer_id, message, submission_time, username)
    VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(username)s)""",
        {
            "submission_time": submission_time,
            "answer_id": answer_id,
            "message": message,
            "username": username
        }
    )


@database_common.connection_handler
def create_user_registration(cursor, username, password_hash):
    date_of_registration = controller.date_and_time()
    cursor.execute(f"""
    INSERT INTO users(username, password_hash, date_of_registration, reputation) 
    VALUES (%(username)s, %(password_hash)s, %(date_of_registration)s, 0)
      """, {
        'username': username,
        'password_hash': password_hash,
        'date_of_registration': date_of_registration,

        }
    )
    return


@database_common.connection_handler
def username_exist(cursor, username):
    cursor.execute("""
    SELECT username from users
    """)
    list_of_all_users = [user['username'] for user in cursor.fetchall()]
    return username in list_of_all_users


@database_common.connection_handler
def search(cursor, search_phrase):
    cursor.execute(f"""
    SELECT * FROM question
    WHERE message LIKE %(search_phrase)s OR title LIKE %(search_phrase)s
    """, {
        "search_phrase": f"%{search_phrase}%"
    })
    return cursor.fetchall()


@database_common.connection_handler
def search_answer(cursor, search_phrase):
    cursor.execute(f"""
    SELECT * FROM answer
    WHERE message LIKE %(search_phrase)s
    """, {
        "search_phrase": f"%{search_phrase}%"
    })
    return cursor.fetchall()


@database_common.connection_handler
def get_last_5_questions(cursor):
    cursor.execute(
        f"""
    SELECT * FROM question
    ORDER BY submission_time DESC
    LIMIT 5;
    """,
    )
    return cursor.fetchall()


@database_common.connection_handler
def add_tag(cursor, tag):
    query = """
        SELECT id
        FROM tag
        WHERE name = %(tag)s
    """
    values = {"tag": tag}
    cursor.execute(query, values)
    tag_id = cursor.fetchone()
    if tag_id is None:
        query = """
            INSERT INTO tag (name)
            VALUES (%(tag)s)
            RETURNING id
        """
        cursor.execute(query, values)
        tag_id = cursor.fetchone()
    return tag_id['id']


@database_common.connection_handler
def update_question_tag_table(cursor, question_id, tag_id):
    cursor.execute(f"""
    INSERT INTO question_tag(question_id, tag_id)
    VALUES (%(question_id)s, %(tag_id)s)
    """,
                   {
                       "question_id": question_id,
                       "tag_id": tag_id
                   }
    )


@database_common.connection_handler
def get_question_tags(cursor, question_id):
    tags = []
    query = """
        SELECT tag_id
        FROM question_tag
        WHERE question_id = %(id)s
   """

    values = {
        "id": question_id
    }
    cursor.execute(query, values)
    ids = cursor.fetchall()

    query1 = """
        SELECT *
        FROM tag
        WHERE id = %(id)s
    """
    for idz in ids:
        values1 = {
            "id": idz["tag_id"]
        }
        cursor.execute(query1, values1)
        tags.append(cursor.fetchone())
    return tags


@database_common.connection_handler
def get_hashed_password(cursor, username):
    cursor.execute(""" 
            SELECT password_hash FROM users
            WHERE username = %(username)s
            """, {'username': username})
    hashed_password = cursor.fetchone()
    return hashed_password['password_hash']


@database_common.connection_handler
def get_all_users_attributes(cursor):
    cursor.execute(""" 
        SELECT * FROM users
        ORDER BY username
        """)
    users = cursor.fetchall()

    return users


@database_common.connection_handler
def get_one_user_attributes(cursor, username):
    cursor.execute("""
        SELECT * FROM users
        WHERE username = %(username)s
        """, {'username': username})
    user = cursor.fetchone()

    return user


@database_common.connection_handler
def get_data_by_username(cursor, table, username):
    cursor.execute(
        f"""
      SELECT * FROM {table}
      WHERE username = %(username)s;
      """,
        {"username": username}
    )
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def update_question_view(cursor, question_id):
    cursor.execute(f"""
    UPDATE question
    SET view_number = view_number + 1
                        WHERE id = %(question_id)s
    """,
                   {"question_id": question_id}
    )


@database_common.connection_handler
def bind_question_to_user(cursor, question_id, user):
    cursor.execute(f"""
    SELECT username from question
    WHERE question_id = %(question_id)s """)


@database_common.connection_handler
def register_question_vote_and_reputation(cursor, question_id, vote, username):
    cursor.execute("""
                   UPDATE question SET vote_number = vote_number + %(vote)s
                   WHERE id= %(question_id)s
                   """,
                   {"question_id": question_id, "vote": vote})

    reputation = vote
    if vote == -1:
        reputation = -2
    elif vote == 1:
        reputation = 5

    cursor.execute("""
            UPDATE users
            SET reputation = 
            (SELECT reputation 
            FROM users 
            WHERE username = %(username)s) + %(reputation)s
            WHERE username = %(username)s

            """, {'username': username, 'reputation': reputation})


@database_common.connection_handler
def register_answer_vote_and_reputation(cursor, answer_id, question_id, vote, username):
    cursor.execute("""
                   UPDATE answer SET vote_number = vote_number + %(vote)s
                   WHERE id= %(answer_id)s and question_id = %(question_id)s
                   """,
                   {"answer_id": answer_id, "question_id": question_id, "vote": vote})

    reputation = vote
    if vote == -1:
        reputation = -2
    elif vote == 1:
        reputation = 10

    cursor.execute("""
            UPDATE users
            SET reputation = 
            (SELECT reputation 
            FROM users 
            WHERE username = %(username)s) + %(reputation)s
            WHERE username = %(username)s

            """, {'username': username, 'reputation': reputation})