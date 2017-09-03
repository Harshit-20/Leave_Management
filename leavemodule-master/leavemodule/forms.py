from django import forms;
from  . models import Leave, ApplicationRequest, RemainingLeaves;
from django.contrib.auth.models import User;
from django.contrib.auth.forms import UserCreationForm;
from datetime import datetime


class UserForm(forms.ModelForm):
	class Meta:
		model =  User;
		fields = ('username', 'email');

class LeaveForm(forms.ModelForm):
	# def __init__(self, *args, **kwargs):
	# 	if 'user' in kwargs.keys():
	# 		self.user = kwargs.pop('user');
	class Meta:
		model = Leave;
		fields = ('leave_type', 'replacing_user', 'start_date', 'end_date', 'purpose', 'leave_address');
		widgets = {
			'start_date': forms.SelectDateWidget(),
			'end_date': forms.SelectDateWidget(),
			'purpose': forms.Textarea,
		}
	
	def clean(self):
		replacing_user = self.cleaned_data['replacing_user']
		#if replacing_user == self.user:
		#	raise forms.ValidationError('Cant choose yourself as replacing user')
		
		try:
			start_date = self.cleaned_data['start_date'];
			end_date = self.cleaned_data['end_date'];
			leave_type = self.cleaned_data['leave_type'];

		except KeyError:
			raise forms.ValidationError('Invalid Input');
        

		if start_date > end_date or start_date.strftime("%m%d%Y") < datetime.now().strftime("%m%d%y"):
			raise forms.ValidationError('Invalid Dates Entered')
		
		leave_days = (end_date - start_date).days+1;

		if leave_type == 'station':
			if self.cleaned_data['leave_address']=='':
				raise forms.ValidationError('If on Station Leave, specify Leave address');
			elif leave_days > 2:
				raise forms.ValidationError('Maximum 2 Station leaves at a time is allowed');
			elif start.date.weekday() not in [5, 6] or end_date.weekday() not in [5, 6]:
				raise forms.ValidationError('Only weekend leaves taken as Station Leaves');
		elif leave_type == 'vacation':
			if not (start_date.strftime("%m%d") > "05/05" and end_date.strftime("%m%d")<"07/25"):
				raise forms.ValidationError("Vacation Leaves can be taken only in vaction period, (05 may to 25 july)");
		'''
		RemainingLeaves.objects.create(user=self.user)
		user_leave_data = RemainingLeaves.objects.get(user=self.user)
		remaining_leaves = getattr(user_leave_data, type_of_leave, 2)
		print(leave_days, remaining_leaves)
		if leave_days > remaining_leaves:
			raise forms.ValidationError('Only {} {} leaves remaining'.format(remaining_leaves, self.cleaned_data['type_of_leave']))
		'''