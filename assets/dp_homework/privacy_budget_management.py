import opendp.prelude as dp
from random import randint

dp.enable_features('contrib')

privacy_unit = dp.unit_of(contributions=1)
privacy_loss = dp.loss_of(epsilon=1)
bounds = (0.0, 100.0)
imputed_value = 50.0

data = [float(randint(0, 100)) for _ in range(100)]

context = dp.Context.compositor(
    data=data,
    privacy_unit=privacy_unit,
    privacy_loss=privacy_loss,
    split_evenly_over=10
)

loop_count = 0

while True:
    loop_count += 1
    print(loop_count)
    count_query = (
        context.query()
        .count()
        .laplace()
    )
    dp_count = count_query.release()
    mean_query = (
        context.query()
        .clamp(bounds)
        .resize(size=dp_count, constant=imputed_value)
        .mean()
        .laplace()
    )
    dp_mean = mean_query.release()
