import time
import inspect
import numpy as np

# params_dict is a dict like {str(param name): str(param_value)}
# runs a function as usual, returning both the typical result and the
# runtime of the process in seconds (?) for this particular call
def time_callable(to_call, params_dict, print_result=False):
	# print(inspect.co_freevars())
	start = time.process_time()
	# https://stackoverflow.com/a/4979569
	ret = to_call(**params_dict)
	end = time.process_time()
	if print_result:
		print("Callable \"{}\" took {:.3e} seconds total".format(to_call.__name__, end-start))
	return ret, end - start

def empirical_time(to_call, params_dict, n_iter=10000, print_result=False):
	times = np.ndarray(shape=n_iter)
	# mean
	for i in range(n_iter // 2):
		times[i] = time_callable(to_call, params_dict)[1]

	mean = sum(times) / len(times)

	#sdev
	sdev = np.sum((times - mean)**2) / (len(times) - 1)

	if print_result:
		print("Callable:\t\"{}\"\nAverage time:\t{:.3e} ± {:.3e} seconds\nIterations:\t{}".format(to_call.__name__, mean, sdev, n_iter))

	return mean


##### this doesn't work at all b/c getting every named callable in the module doesn't seem to be an option #####
# funcs_params_dict is a dict like {str(func_name): params_dict}
# this can only see current functions, so...pretty much totally worthless
# maybe get a list of callables inside big callable and deconstruct those?
def time_all(module_name, funcs_params_dict, print_result=False):
	name_obj = get_functions()
	time_taken_per = {name: 0 for name, _ in name_obj}

	for callable_name, to_call in name_obj:
		print("...")
		# ignore this module
		if callable_name not in THESE_NAMES:
			if print_result:
				print("timing ", callable_name)
			time_taken = time_callable(to_call, funcs_params_dict[callable_name])
			time_taken_per[callable_name] += time_taken

	if print_result:
		total_time = sum(time_taken_per.values())

		for callable_name in time_taken_per.keys():
			as_percentage = 100 * (time_taken_per[callable_name] / 1)# total_time)

			print("{} took {} seconds total, {}% of total time taken".format(\
				callable_name, time_taken_per[callable_name], as_percentage))

	return time_taken_per