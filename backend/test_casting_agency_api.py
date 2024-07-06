import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from src import create_app
from src.database.models import setup_db, Movie, Actor
from dotenv import load_dotenv

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.database_name = os.getenv("DB_NAME_TEST")
        self.database_url = os.getenv("DB_URL")
        self.database_path = "postgresql://{}/{}".format(self.database_url, self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        self.assistant={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRkWTVMMlIxbkZoM1BBVTdPZG0tRyJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjgyN2IwMWExMzk3NGE0ZDIxNjQ1ZWQiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MjAyNzUxNzgsImV4cCI6MTcyMDM2MTU3OCwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF6cCI6IkVKQlZ3aG83TWRjZnVvaGtaMEdXWXE3bHpRbzVDMmxUIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.d0U73XKTMHNb69pi4XMxr5YAn8EMJlG116vIxDFyqg-fn_G1bKiv31-WidzyRsRARNvgZxpwDFUNrcX2rf1Y3_EvqLhmv7xXaZpDNsouwCfxyvtLZVp9ddMyR8Kv6ypsl7pLszR93s89guoRqbv1UMWDkt9uYjcXZCCKNO26IBIBVMHu9y2z-Fox18thP74wXtFs1lerRt1zhoPyB5tgy7AO1-aLbUMQnRXqdNiPuMzJ5u7EfHoZQx00XeacSkT4D4CGFMunwyrxvG9DjqCJyUf2NO8Zi2PFvwS7cM9kDcXUW8NQr9fajXxYNtaeR0oOzD32U3373oobGX90buG98w'}
        self.director={'Authorization': 'Bearer  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRkWTVMMlIxbkZoM1BBVTdPZG0tRyJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjgyN2EzYWUwMGY3NGQwNmIwMTlmZjEiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MjAyNzk5OTMsImV4cCI6MTcyMDM2NjM5Mywic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF6cCI6IkVKQlZ3aG83TWRjZnVvaGtaMEdXWXE3bHpRbzVDMmxUIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvcnMiXX0.hZDkBelSfpNHACyGlUwwgKowPas6KDKeUNEeHk9D1bUEZCMVKTHsBsDa9tNfm0M8MvFoQlSR4zwBDt10pqUuG290UHvvr1Gfz1QjXbJc04rT4OBHaHfwZSfoUiUgeWQPkO-v69qrSk2Gr2UjIKaWhUfhQpqpWYnsJ203l_h6fNegfO184ZNgaMdk_fNq-JPEH_FhIuxZ4x9shoLOHvsyG0_hEaPkK-zKzy4yGZMcAU-bOFp8lo_cmlQx11wuXJiBu4flHdSHQ6bY1bvXt0Dj-F4QRzCOcdn9yXEkh85gcoZF1s6ebLN1syglhiZkn2AZgKIYAtpD9RrXZxoajm75pQ'}
        self.authHeader={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRkWTVMMlIxbkZoM1BBVTdPZG0tRyJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMmhqMmwzemgzNm9kemRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNDIzNDk0NzIwNjM3Mzc2NDkxMCIsImF1ZCI6WyJjYXN0aW5nLWFnZW5jeSIsImh0dHBzOi8vZGV2LWEyaGoybDN6aDM2b2R6ZG8udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcyMDI3MzEzNSwiZXhwIjoxNzIwMzU5NTM1LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoiRUpCVndobzdNZGNmdW9oa1owR1dZcTdselFvNUMybFQiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.I6-OPaZQGMqG6uD0sePbzgskBIO5uTNpZVYDtZfGfHS3Z6_Q2wZ9eD_Lke2C6oScpH9Rh378TkP6LXaBOUkc_QGGYSO_llm6b3-FsI9zHCfNxAMthlTcjhzUiQ1p2HshNp0mSLvau_foGbfFR8UIRD9C4z0ianpWD1bhgCqiKxhSd4YV3eAzOocGtCHl4WEP4T3SeOPrDBUwW3_xTaoHYNoLDUp2dXg739fULuXmUdNQQ-vFrA2tllQdk32xa7qk1zE-pRSB4FcW9pBvf_SW4R2dG62L02FfJoJ61xeFFTIGknQ0uesPihseD7eF6KNSQ1CxpWhvWKGzsrij6pvGlg'}
        
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