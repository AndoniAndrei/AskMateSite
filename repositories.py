import controller
import database_common


@database_common.connection_handler
def get_all_data(cursor, table, order_by, direction):
    cursor.execute(
        f"""
     SELECT * FROM {table}
     ORDER BY {order_by} {direction}
     """
    )
    data = cursor.fetchall()
    return data


@database_common.connection_handler
def get_data_by_question_id(cursor, table, data_id):
    column = "id"
    if table == "answer":
        column = "question_id"
    if table == "comment":
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
def add_new_question(cursor, title, message, image):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
    VALUES (%(submission_time)s,0, 0, %(title)s, %(message)s, %(image)s)
    """,
        {
            "submission_time": submission_time,
            "title": title,
            "message": message,
            "image": image,
        },
    )


@database_common.connection_handler
def add_new_answer(cursor, message, image, question_id):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO answer(submission_time, vote_number, question_id, message, image)
    VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s) """,
        {
            "submission_time": submission_time,
            "message": message,
            "image": image,
            "question_id": question_id,
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
def edit_question(cursor, table, item_id, title, message, image):
    column = "id"
    cursor.execute(
        f"""
    UPDATE {table}
    SET title = %(title)s, message = %(message)s, image = %(image)s
    WHERE {column} = %(id)s 
    """,
        {"message": message, "title": title, "image": image, "id": item_id},
    )

@database_common.connection_handler
def edit_answer(cursor, answer_id, message):
    cursor.execute(f"""
    UPDATE answer SET message = %(message)s
    WHERE id = %(id)s
        """,
                   {"id" : answer_id, "message" : message}
    )


@database_common.connection_handler
def edit_comment(cursor, comment_id, message):
    cursor.execute(f"""
        UPDATE comment SET message = %(message)s
        WHERE id = %(id)s
            """,
                   {"id": comment_id, "message": message}
                   )


@database_common.connection_handler
def register_question_vote(cursor, question_id, vote):
    cursor.execute("""
                   UPDATE question SET vote_number = vote_number + %(vote)s
                   WHERE id= %(question_id)s
                   """,
                   {"question_id": question_id, "vote": vote})


@database_common.connection_handler
def register_answer_vote(cursor, answer_id,question_id, vote):
    cursor.execute("""
                   UPDATE answer SET vote_number = vote_number + %(vote)s
                   WHERE id= %(answer_id)s and question_id = %(question_id)s
                   """,
                   {"answer_id": answer_id, "question_id": question_id, "vote": vote})


@database_common.connection_handler
def add_comment_question(cursor, question_id, message):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO comment(submission_time, question_id, message)
    VALUES (%(submission_time)s, %(question_id)s, %(message)s)""",
        {
            "submission_time": submission_time,
            "message": message,
            "question_id": question_id,
        },
        )


@database_common.connection_handler
def add_comment_answer(cursor, answer_id, message):
    submission_time = controller.date_and_time()
    cursor.execute(
        f"""
    INSERT INTO comment(answer_id, message, submission_time)
    VALUES (%(answer_id)s, %(message)s, %(submission_time)s)""",
        {
            "submission_time": submission_time,
            "answer_id" : answer_id,
            "message" : message
        }
        )


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
def get_last_5_questions(cursor):
    cursor.execute(
        f"""
    SELECT * FROM question
    ORDER BY submission_time DESC
    LIMIT 5;
    """,
    )
    return cursor.fetchall()

# @database_common.connection_handler
# def delete_comment(cursor, question_id):
#     cursor.execute(f"""
#     DELETE from comment, message = %(message)s
#         WHERE id = %(id)s
#     """,
#     )
#     return cursor.fetchall()