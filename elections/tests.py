from django.test import TestCase

from .models import Voivodeship, Vote, Community, Candidate

from django.core.exceptions import ValidationError
# Create your tests here.

class VoivodeshipMethodTests(TestCase):

	def setUp(self):

		voi_1 = Voivodeship.objects.create(name='test', 
										 citizens=1000, 
										 allowed=1001, 
										 voting_cards=998, 
										 votes=997, 
										 valid_votes=996, 
										 votes_for_cand_1=995, 
										 votes_for_cand_2=1)

		voi_2 = Voivodeship.objects.create(name='test2', 
										 citizens=1000, 
										 allowed=999, 
										 voting_cards=1000, 
										 votes=997, 
										 valid_votes=996, 
										 votes_for_cand_1=995, 
										 votes_for_cand_2=1)

		voi_3 = Voivodeship.objects.create(name='test3', 
										 citizens=1000, 
										 allowed=999, 
										 voting_cards=998, 
										 votes=1000, 
										 valid_votes=996, 
										 votes_for_cand_1=995, 
										 votes_for_cand_2=1)

		voi_4 = Voivodeship.objects.create(name='test4', 
										 citizens=1000, 
										 allowed=999, 
										 voting_cards=998, 
										 votes=997, 
										 valid_votes=1000, 
										 votes_for_cand_1=995, 
										 votes_for_cand_2=1)


	def test_if_percent_1_and_percent_2_sum_up_correctly(self):

		voi = Voivodeship.objects.get(name='test')
		self.assertEqual(voi.percent_1() + voi.percent_2(), 100)

	def test_if_not_less_citizens_than_allowed(self):

		voi = Voivodeship.objects.get(name='test')
		self.assertRaises(ValidationError, voi.clean)


	def test_if_not_less_allowed_than_voting_cards(self):

		voi = Voivodeship.objects.get(name='test2')
		self.assertRaises(ValidationError, voi.clean)

	def test_if_not_less_voting_cards_than_votes(self):

		voi = Voivodeship.objects.get(name='test3')
		self.assertRaises(ValidationError, voi.clean)

	def test_if_not_less_votes_than_valid_votes(self):
		
		voi = Voivodeship.objects.get(name='test4')
		self.assertRaises(ValidationError, voi.clean)



class CommunityMethodTests(TestCase):

	def setUp(self):

		voi = Voivodeship.objects.create(name='test', citizens=2000, allowed=0, voting_cards=0, votes=0, valid_votes=0, votes_for_cand_1=50, votes_for_cand_2=30)
		comm_1 = Community.objects.create(name='test2', 
										voivodeship_ptr=voi,
										citizens=1000,
										allowed=1001)

		comm_2 = Community.objects.create(name='test3', 
										voivodeship_ptr=voi,
										citizens=4000,
										allowed=1001)

		vote = Vote.objects.create(community_ptr=comm_1)

	def test_get_votes(self):

		voi = Voivodeship.objects.get(name='test')
		comm = Community.objects.get(name='test2')
		vote = Vote.objects.get(community_ptr=comm)
		self.assertEqual(comm.get_votes(), vote)


	def test_if_not_less_citizens_than_allowed(self):

		voi = Voivodeship.objects.get(name='test')
		comm = Community.objects.get(name='test2')
		self.assertRaises(ValidationError, comm.clean)


	def test_if_not_less_citizens_in_voi_than_in_comm(self):
		
		voi = Voivodeship.objects.get(name='test')
		comm = Community.objects.get(name='test3')
		self.assertRaises(ValidationError, comm.clean)



class VoteMethodTests(TestCase):

	def setUp(self):

		voi = Voivodeship.objects.create(name='test', citizens=0, allowed=0, voting_cards=0, votes=0, valid_votes=0, votes_for_cand_1=50, votes_for_cand_2=30)
		comm = Community.objects.create(name='test2', allowed = 705, voivodeship_ptr=voi)
		comm_2 = Community.objects.create(name='test3', allowed = 705, voivodeship_ptr=voi)
		comm_3 = Community.objects.create(name='test4', allowed = 705, voivodeship_ptr=voi)
		vote = Vote.objects.create(community_ptr=comm,
								 voting_cards = 710,
								 votes = 701,
								 valid_votes = 700,
								 votes_for_cand_1 = 300, 
								 votes_for_cand_2 = 400)

		vote_2 = Vote.objects.create(community_ptr=comm_2,
								 voting_cards = 700,
								 votes = 701,
								 valid_votes = 700,
								 votes_for_cand_1 = 300, 
								 votes_for_cand_2 = 400)

		vote_3 = Vote.objects.create(community_ptr=comm_3,
								 voting_cards = 700,
								 votes = 700,
								 valid_votes = 701,
								 votes_for_cand_1 = 300, 
								 votes_for_cand_2 = 400)

	def test_if_percent_1_and_percent_2_sum_up_correctly(self):

		voi = Voivodeship.objects.get(name='test')
		comm = Community.objects.get(name='test2')
		vote = Vote.objects.get(community_ptr=comm)
		self.assertEqual(vote.percent_1() + vote.percent_2(), 100)


	def test_if_not_less_voting_cards_than_allowed(self):
		
		voi = Voivodeship.objects.get(name='test')
		comm = Community.objects.get(name='test2')
		vote = Vote.objects.get(community_ptr=comm)
		self.assertRaises(ValidationError, vote.clean)

	def test_if_not_less_votes_than_voting_cards(self):
		
		voi = Voivodeship.objects.get(name='test')
		comm = Community.objects.get(name='test3')
		vote = Vote.objects.get(community_ptr=comm)
		self.assertRaises(ValidationError, vote.clean)

	def test_if_not_less_valid_votes_than_votes(self):

		voi = Voivodeship.objects.get(name='test')
		comm = Community.objects.get(name='test4')
		vote = Vote.objects.get(community_ptr=comm)
		self.assertRaises(ValidationError, vote.clean)


class CandidateMethodTests(TestCase):

	def setUp(self):

		can_1 = Candidate.objects.create(first_name = 'test1', middle_name = 'test1', last_name = 'test1')
		can_2 = Candidate.objects.create(first_name = 'test2', middle_name = 'test2', last_name = 'test2')
		can_3 = Candidate.objects.create(first_name = 'test3', middle_name = 'test3', last_name = 'test3')

	def test_if_not_more_than_two_candidates(self):

		can = Candidate.objects.get(first_name = 'test1')

		self.assertRaises(ValidationError, can.clean)	


# Selenium tests

import time
from selenium import webdriver
from django import test

class SeleniumTests(test.LiveServerTestCase):

	def test_loading_page(self):
		browser = webdriver.Chrome()
		browser.get('http://127.0.0.1:8000/elections')

		result = "Wybory 2005" in browser.title

		time.sleep(1)

		if result:
		    print("Test 1 passed")
		else:
		    print("Test 1 failed")

		browser.quit()

	def test_loading_with_fake_data(self):

		browser = webdriver.Chrome()
		browser.get('http://127.0.0.1:8000/elections')

		try:
		    logout = browser.find_element_by_id("logout")
		    if logout is not None:
		        logout.click()
		except:
		    pass

		login = browser.find_element_by_id("login")
		login.click()

		browser.get('http://127.0.0.1:8000/elections/login')

		user = browser.find_element_by_name("username")
		user.send_keys('asdasdasdasd')
		passw = browser.find_element_by_name("password")
		passw.send_keys('asdasdasdasd')
		send = browser.find_element_by_id("submit")
		send.click()

		browser.get('http://127.0.0.1:8000/elections')
		try:
		    login = browser.find_element_by_id("login")
		    print("Test 2 passed")
		except:
		    print("Test 2 failed")

		browser.quit()	

	def test_two_mods_simulteanously(self):

		b1 = webdriver.Chrome()
		b1.get('http://127.0.0.1:8000/elections')

		b2 = webdriver.Chrome()
		b2.get('http://127.0.0.1:8000/elections')

		try:
		    b1.find_element_by_id("logout").click()
		except:
		    pass

		try:
		    b2.find_element_by_id("logout").click()
		except:
		    pass

		# logging in
		b1.find_element_by_id("login").click()
		time.sleep(1)
		b1.find_element_by_name("username").send_keys('testuser')
		b1.find_element_by_name("password").send_keys('test1234')
		b1.find_element_by_id("submit").click()

		b2.find_element_by_id("login").click()
		time.sleep(1)
		b2.find_element_by_name("username").send_keys('testuser')
		b2.find_element_by_name("password").send_keys('test1234')
		b2.find_element_by_id("submit").click()

		time.sleep(5)

		# Editing Bitowice in browser 1

		try:
		    voi = b1.find_element_by_id("mazowieckie")
		    voi.click()


		    time.sleep(1)
		    comm = b1.find_element_by_id("Bitowice")

		    comm.click()
		    voting_cards = 200
		    votes = 200
		    valid = 200
		    cand_1 = 100
		    cand_2 = 100

		    b1.find_element_by_id("inputVotingCards").send_keys(str(voting_cards))
		    b1.find_element_by_id("inputVotes").send_keys(str(votes))
		    b1.find_element_by_id("inputValidVotes").send_keys(str(valid))
		    b1.find_element_by_id("inputVotesForCand1").send_keys(str(cand_1))
		    b1.find_element_by_id("inputVotesForCand2").send_keys(str(cand_2))
		except:
		    print("Test 5 failed")

		time.sleep(1)

		# Editing Bitowice in browser 2

		try:
		    voi = b2.find_element_by_id("mazowieckie")
		    voi.click()


		    time.sleep(1)
		    comm = b2.find_element_by_id("Bitowice")

		    comm.click()
		    voting_cards = 200
		    votes = 200
		    valid = 200
		    cand_1 = 100
		    cand_2 = 100

		    b2.find_element_by_id("inputVotingCards").send_keys(str(voting_cards))
		    b2.find_element_by_id("inputVotes").send_keys(str(votes))
		    b2.find_element_by_id("inputValidVotes").send_keys(str(valid))
		    b2.find_element_by_id("inputVotesForCand1").send_keys(str(cand_1))
		    b2.find_element_by_id("inputVotesForCand2").send_keys(str(cand_2))
		    b2.find_element_by_id("submit").click()

		    b1.find_element_by_id("submit").click()
		    not_edited = b1.find_element_by_id("not-edited")
		    print(not_edited.data-msg)
		    if ("edytowal dane" in not_edited.data-msg):
		        print("Test 3 failed")
		    else:
		        print("Test 3 passed")
		    time.sleep(2)
		except:
		    print("Test 3 passed")

		# exiting browsers
		b1.quit()
		b2.quit()



