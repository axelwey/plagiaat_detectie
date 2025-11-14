months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
new_months=[month for month in months if len(month)<6]
print(new_months)
new2_months=[f"({index}: {month[:3].upper()})" for index, month in enumerate(new_months,start=1)]
print(new2_months)