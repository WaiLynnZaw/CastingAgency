import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from src import create_app
from src.database.models import setup_db, Movie, Actor

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = os.environ['DATABASE_URL_TEST']
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        self.assistant={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRkWTVMMlIxbkZoM1BBVTdPZG0tRyJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjgyN2IwMWExMzk3NGE0ZDIxNjQ1ZWQiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MjAzMjI4MTYsImV4cCI6MTcyMDQwOTIxNiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF6cCI6IkVKQlZ3aG83TWRjZnVvaGtaMEdXWXE3bHpRbzVDMmxUIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.oux2IekXSacgJ-UFpjsHH7H-6O7qnRKUMr2G0zBpzEksLZQDHbasWQ523ilboTHPFPUcR3x3dUBImmlqIUNe-swPV82ir__zXhh7FWaPd1jcfRqjLf05KjuVJvKucBRpCE-Aq9eFn_npPZFfZh8tKOmou_9l8eSzM2uyUip4X0_4oFjHxh2EFDE4Ji2ZdvmmH8Po3alXvLOKH9gWS1sS4vvqxCfoLPkzMJiyFOWI_yknxo-8SIQEQBWD2TeUv0LQmhiAff0Bgyy0hn1g2QigJEGfGTRXbsyDUuFls0cNxb8nmhK8qYQwdTH9S3KIbbWDk436Cf7AYEzxhdX7LX2TmA'}
        self.director={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRkWTVMMlIxbkZoM1BBVTdPZG0tRyJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjgyN2EzYWUwMGY3NGQwNmIwMTlmZjEiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MjAzMjI4NjMsImV4cCI6MTcyMDQwOTI2Mywic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF6cCI6IkVKQlZ3aG83TWRjZnVvaGtaMEdXWXE3bHpRbzVDMmxUIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvcnMiXX0.A0PHssfmC_chgD9mJal9q5uRGu6GiqJWy2Iwm3KDcsBpdV4EJCsxwx3R4XJXoAuXqYCq6lgALE3KyM5pqRdPxgYnEHpweM8iKBZ2TJby7nFoMhlZVPoEqYyS1N7RLT8rjWH3rF2LunOZ2PMFGAeG6H32NxzXmtodMsKGqI8piW65VaJ2mkM-jI9KfMWuoRXtMegtw2aQZ9eUl1GPVRIn66SeLSeDMNnL5Cik3B-o6SSntL893uzt-_xyrkgGylgohpTwoMFBNpOQRAOjxQa_ho_0uQiB3rYvW-uUeXPUYP93vIscv5ah4waLMwbk2FQEmavZ6mofvow4lUr3ovTUoQ'}
        self.authHeader={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRkWTVMMlIxbkZoM1BBVTdPZG0tRyJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjgyN2I3OTgwN2FlMDQwZGUzNmY5ZGQiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MjAzMjI2MDMsImV4cCI6MTcyMDQwOTAwMywic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF6cCI6IkVKQlZ3aG83TWRjZnVvaGtaMEdXWXE3bHpRbzVDMmxUIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.t4joloZk9FLsW2WBP6S6-Cao9ZWJYef6hoYCrGlBa3WpN7V6PpZDs-FlgrhKLNitRZM4AJkfAwEmZpCsNGv5gZUzkIuRKspsGDxMYMTz_doEzeoWx1hQrfa2mdI1SzjhqkiRYkxhGCls5-t14tzvBh5Tewl8rSWiyI7a4CWMUMJKiKE2I30ZBAwSTjBR3cPjhEfCK15CtzBmHqVoqIrngL-pyHnzFMYkf_PFGvR4EFrRDEInfVZBmpRH9PJui65eEBg8uWfDjIuctKdVkTFTBgPznioyqu0RSbcdtFNUoxZuTsFPi3MhRVg38FcsvQz2Zcn0fzj9tOfdGBXU7GH5fw'}
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_movie = {"title":"We bare bears", "release_date":"2023-06-06"}
        self.update_movie = {"title":"We bare bears", "release_date":"2024-06-06"}
        self.new_actor = {"name": "Grizz", "age": 5, "gender": "Male"}
        self.update_actor = {"name": "IceBear", "age": 5, "gender": "Male"}


    def tearDown(self):
        """Executed after reach test"""
        self.db.drop_all()
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', 
                      headers=self.authHeader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_fail_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        
    def test_add_movie(self):
        res = self.client().post('/movies', 
                                 json=self.new_movie,
                                 headers=self.authHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_fail_add_movie(self):
        res = self.client().post('/movies', 
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        res = self.client().patch('/movies/1', 
                                 json=self.update_movie,
                                 headers=self.authHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_fail_update_movie(self):
        res = self.client().patch('/movies/1', 
                                 json=self.update_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        
    def test_delete_movie(self):
        res = self.client().delete('/movies/1',
                                   headers=self.authHeader)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)
        
    def test_fail_delete_movie(self):
        res = self.client().delete('/movies/999',
                                   headers=self.authHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    # Actor    
    def test_get_actors(self):
        res = self.client().get('/actors', 
                      headers=self.authHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_fail_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        
    def test_add_actor(self):
        res = self.client().post('/actors', 
                                 json=self.new_actor,
                                 headers=self.authHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_fail_add_actor(self):
        res = self.client().post('/actors', 
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_actor(self):
        res = self.client().patch('/actors/1', 
                                 json=self.update_actor,
                                 headers=self.authHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_fail_update_actor(self):
        res = self.client().patch('/actors/1', 
                                 json=self.update_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        
    def test_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers=self.authHeader)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)
        
    def test_fail_delete_actor(self):
        res = self.client().delete('/actors/999',
                                   headers=self.authHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    #RBAC
    # Casting Assistant Role - Only Read Permission.
    def test_assistant_get_movie(self):
        res = self.client().post('/validate_permission', 
                      headers=self.assistant,
                      json={'permission': 'get:movies'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    
    def test_assistant_get_actor(self):
        res = self.client().post('/validate_permission', 
                      headers=self.assistant,
                      json={'permission': 'get:actors'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
    def test_fail_assistant_update(self):
        res = self.client().post('/validate_permission', 
                      headers=self.assistant,
                      json={'permission': 'patch:movie'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        
    def test_fail_assistant_delete(self):
        res = self.client().post('/validate_permission', 
                      headers=self.assistant,
                      json={'permission': 'delete:movie'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        
    # Casting Director Role - Able to modify movie, but cannot delete
    def test_director_update_movie(self):
        res = self.client().post('/validate_permission', 
                      headers=self.director,
                      json={'permission': 'patch:movie'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
    def test_director_fail_delete_movie(self):
        res = self.client().post('/validate_permission', 
                      headers=self.director,
                      json={'permission': 'delete:movie'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        
    # Executive Producer Role - Can do all.
    def test_producer_delete_movie(self):
        res = self.client().post('/validate_permission', 
                      headers=self.authHeader,
                      json={'permission': 'delete:movie'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
    def test_producer_delete_actor(self):
        res = self.client().post('/validate_permission', 
                      headers=self.authHeader,
                      json={'permission': 'delete:actor'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()