import pickle
import numpy as np
import pandas as pd

def get_hard_coded_job(industry_dict, database):
	# Hard coding to speed things up
	if occupation == "retired":
		return "retired"
	elif "software" in occupation:
		return industry_dict[12]
	elif "engineer" in occupation or "professor" in occupation or "faculty" in occupation:
		return industry_dict[9]
	elif "attorney" in occupation or "lawyer" in occupation:
		return industry_dict[2]
	elif "doctor" in occupation or "surgeon" in occupation:
		return industry_dict[6]
	elif "manager" in occupation or "owner" in occupation:
		return industry_dict[7]
	elif "real estate" in occupation:
		return industry_dict[8]
	elif "construction" in occupation:
		return industry_dict[17]
	elif "bank" in occupation:
		return industry_dict[3]
	elif occupation in database.keys():
		if len(str(database[occupation])) < 3 and str(database[occupation]) != "na":
			return industry_dict[int(database[occupation])]
		return database[occupation]
	return None

def make_database():
	with open("database.pkl", "rb+") as f:
		return pickle.load(f)

def get_industries():
	industries = []
	with open("industries.txt", "r") as f:
		for line in f.readlines():
			industries.append(line.strip("\n").lower())

	return industries

def get_frequency(industries, database):
	frequencies = dict()
	for industry in industries:
		frequencies[industry] = 0

	total = 0
	for entry in database:
		industry = database[entry]

		if len(str(industry)) < 3 and str(industry) != "na":
			industry = industries[int(industry)]

		frequencies[industry] += 1
		total += 1

	for industry in industries:
		frequencies[industry] = frequencies[industry] / total

	return frequencies

def make_keyword_dict(database, industries):

	keywords = dict()
	frequencies = get_frequency(industries, database)
	for entry in database:
		industry = database[entry]

		if len(str(industry)) < 3 and str(industry) != "na":
			industry = industries[int(industry)]

		for word in entry.split():

			if word not in keywords:
				keywords[word] = dict()
				for sector in industries:
					keywords[word][sector] = 2 * frequencies[sector]

			keywords[word][industry] = keywords[word][industry] + 1

	return keywords


def get_score_for_industries(database, industries, occupation, keywords):

	scores = dict()
	for industry in industries:
		scores[industry] = 1

	score = 1
	for word_fragment in occupation.split():

		if word_fragment in keywords:

			total_count = 0
			for industry in keywords[word_fragment]:
				total_count += keywords[word_fragment][industry]

			for industry in industries:
				scores[industry] = scores[industry] * keywords[word_fragment][industry] / total_count

	overall_sum = 0
	for industry in scores:
		overall_sum += scores[industry]

	for industry in scores:
		scores[industry] = scores[industry] / overall_sum


	return scores

def get_candidate(donor_target):
	if "biden" in donor_target or "joe" in donor_target:
		return "Biden"
	if "sanders" in donor_target or "bernie" in donor_target:
		return "Sanders"
	if "warren" in donor_target or "elizabeth" in donor_target:
		return "Warren"
	if "harris" in donor_target or "kamala" in donor_target:
		return "Harris"
	if "buttigieg" in donor_target or "pete" in donor_target:
		return "Buttigieg"
	if "o'rourke" in donor_target or "beto" in donor_target:
		return "O'Rourke"
	if "booker" in donor_target or "cory" in donor_target:
		return "Booker"
	if "klobuchar" in donor_target or "amy" in donor_target:
		return "Klobuchar"
	if "castro" in donor_target or "julian" in donor_target:
		return "Castro"
	if "gillibrand" in donor_target or "kirsten" in donor_target:
		return "Gillibrand"
	if "bennet" in donor_target:
		return "Bennet"
	if "gabbard" in donor_target or "tulsi" in donor_target:
		return "Gabbard"
	if "yang" in donor_target:
		return "Yang"
	else:
		return "rando"
	
if __name__ == '__main__':
	database = make_database()
	industries = get_industries()
	keywords = make_keyword_dict(database, industries)

	#scores = get_score_for_industries(database, industries, job.lower())

	#for key, value in reversed(sorted(scores.items(), key=lambda item: item[1])):
	#	print("%s: %s" % (key, value))

	get_contribution = lambda state, q: pd.read_csv(
		"contribution_data/contributions_q{1}_2019_{0}.csv".format(state, q))
	states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	candidates = ["Biden", "Sanders", "Warren", "Harris", "Buttigieg", "O'Rourke", "Booker", "Klobuchar", "Castro", "Gillibrand", "Bennet", "Gabbard", "Yang"]

	donor_list = set()
	results = dict()
	for candidate in candidates:
		results[candidate] = dict()
		for industry in industries:
			results[candidate][industry] = 0

	for quarter in range(1, 3):
		for state in states:
			print(state, quarter)
			contributions = get_contribution(state, quarter)
			employers = list(contributions["employer"])
			occupations = list(contributions["occupation"])
			committee_names = list(contributions["committee_name"])
			donor_last_name = list(contributions["last_name"])
			donor_first_name = list(contributions["first_name"])

			for i in range(len(employers)):
				donor = str(donor_first_name[i]).lower() + "_" + str(donor_last_name[i]).lower() + "_" + state
				if donor not in donor_list:
					donor_list.add(donor)
					employer = str(employers[i]).lower()
					occupation = str(occupations[i]).lower()
					candidate = get_candidate(str(committee_names[i]).lower())
					if candidate != "rando":
						industry = get_hard_coded_job(industries, database)
						if industry != None:
							results[candidate][industry] += 1
						else:
							industry_odds = get_score_for_industries(database, industries, occupation, keywords)
							for industry in industry_odds:
								results[candidate][industry] += industry_odds[industry]

					if i % 1000 == 0:
						print("\t", str(i) + "/" + str(len(employers)))

	raw_results = np.zeros([len(industries), len(candidates)])
	for i, candidate in enumerate(candidates):
		print(candidate)
		for j, industry in enumerate(industries):
			print("\t", industry, "\t", results[candidate][industry])
			raw_results[j, i] = results[candidate][industry]

	pd.DataFrame(data=raw_results, index=industries, columns=candidates).to_csv("./total_outputs.csv")

	for i, candidate in enumerate(candidates):
		raw_results[0, i] = 0
		raw_results[:, i] = raw_results[:, i] / np.sum(raw_results[:, i])

	pd.DataFrame(data=raw_results[1:], index=industries[1:], columns=candidates).to_csv("./pct_outputs.csv")




