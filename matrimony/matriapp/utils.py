def calculate_match_score(user, potential_match):
    score = 0
    preferences = user.partnerpreference  # Assuming partner preference is linked to user

    # Check gender preferences
    if user.profile.gender == 'Male':
        # For male users, score based on their preferences for female matches
        if potential_match.profile.gender == 'Female':
            # Age preference
            if preferences.min_age <= potential_match.profile.birth_date.year <= preferences.max_age:
                score += 1

            # Height preference
            if preferences.min_height <= potential_match.profile.height <= preferences.max_height:
                score += 1

            # Religion preference
            if preferences.religion == potential_match.profile.religion:
                score += 1

            # Caste preference
            if preferences.caste == potential_match.profile.caste:
                score += 1

            # Education preference
            if preferences.education == potential_match.profile.education:
                score += 1

            # Occupation preference
            if preferences.occupation == potential_match.profile.occupation:
                score += 1

            # Location preference
            if preferences.location == potential_match.profile.location:
                score += 1

    elif user.profile.gender == 'Female':
        # For female users, score based on their preferences for male matches
        if potential_match.profile.gender == 'Male':
            # Age preference
            if preferences.min_age <= potential_match.profile.birth_date.year <= preferences.max_age:
                score += 1

            # Height preference
            if preferences.min_height <= potential_match.profile.height <= preferences.max_height:
                score += 1

            # Religion preference
            if preferences.religion == potential_match.profile.religion:
                score += 1

            # Caste preference
            if preferences.caste == potential_match.profile.caste:
                score += 1

            # Education preference
            if preferences.education == potential_match.profile.education:
                score += 1

            # Occupation preference
            if preferences.occupation == potential_match.profile.occupation:
                score += 1

            # Location preference
            if preferences.location == potential_match.profile.location:
                score += 1

    return score