from script import plot_individual, plot_cumulative, plot_avg

plot_individual(data_dir, 'output/{0}_{1}_{2}'.format(
    params['star_num'][1],
    params['rad'][0],
    params['metallicity'][0]
))
plot_cumulative(data_dir, 'output/{0}_{1}_{2}'.format(
    params['star_num'][1],
    params['rad'][0],
    params['metallicity'][0]
), 'single')
plot_cumulative(data_dir, 'output/{0}_{1}_{2}'.format(
    params['star_num'][1],
    params['rad'][0],
    params['metallicity'][0]
), 'binary')
plot_avg(data_dir, 'output/{0}_{1}_{2}'.format(
    params['star_num'][1],
    params['rad'][0],
    params['metallicity'][0]
), 'single')
plot_avg(data_dir, 'output/{0}_{1}_{2}'.format(
    params['star_num'][1],
    params['rad'][0],
    params['metallicity'][0]
), 'binary')

