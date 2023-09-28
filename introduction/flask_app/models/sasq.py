from flask_app.config.mysqlconnection import connectToMySQL


class Sasq:
  DB = 'user_sasq'

  def __init__(self, data):
    self.id = data['id']
    self.user_id = data['user_id']
    self.location = data['location']
    self.whathappend = data['whathappend']
    self.numberof = data['numberof']
    self.made_at = data.get('made_at')

  @classmethod
  def save (cls, data):
    query = """INSERT into sasq (location, whathappend, numberof, user_id, made_at, created_at, updated_at) 
VALUES ( %(location)s, %(whathappend)s, %(numberof)s, %(user_id)s, %(made_at)s, NOW(),NOW());"""
    results = connectToMySQL('user_sasq').query_db(query, data)
    return results

  @classmethod
  def get_sasq_by_id(cls, id):
    query = """SELECT sasq.id as id, location, whathappend, numberof, made_at, sasq.created_at, sasq.updated_at, user_id, first_name AS posted_by FROM
    sasq JOIN user ON user.id = sasq.user_id WHERE sasq.id = %(id)s;"""
    results = connectToMySQL('user_sasq').query_db(query, {"id": id})
    return cls(results[0])

  @classmethod
  def get_all(cls):
    query = """SELECT sasq.id as id, location, whathappend, numberof, made_at, sasq.created_at, sasq.updated_at, user_id, first_name AS posted_by FROM
    sasq JOIN user ON user.id = sasq.user_id;"""
    results = connectToMySQL('user_sasq').query_db(query)
    if not results:
      return []
    return [cls(row) for row in results]

  @classmethod
  def edit_sasq(cls, data):
    query = """UPDATE sasq SET location%(location)s, whathappend=%(whathappend)s, numberof=%(numberof)s, made_at=%(made_at)s WHERE sasq.id = %(id)s;"""
    results = connectToMySQL('user_sasq').query_db(query, data)
    return results

  @classmethod
  def delete_sasq_by_id(cls, id):
    query = """DELETE FROM recipes WHERE id = %(id)s;"""
    results = connectToMySQL('user_sasq').query_db(query, {"id": id})
    return results

  @staticmethod
  def validate(data):
      errors = []

      required_fields = ('location', 'whathappend', 'numberof', 'made_at')
      for required_field in required_fields:
        if required_field not in data:
          errors.append(f"Missing required field '{required_field}'!")


      if len(data["name"]) < 2:
        errors.append("Name must contain atleast 2 characters.")

      if len(data["instructions"]) < 3:
        errors.append("Instructions must contain atleast 8 characters.")

      if len(data["description"]) < 3:
        errors.append("Description must contain atleast 8 characters.")

      is_valid = len(errors) == 0
      return is_valid, errors