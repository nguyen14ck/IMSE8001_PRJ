library("DBI")
library("RSQLite")

drv <- dbDriver("SQLite")
con <- dbConnect(drv, "data/py_gurobi_r.db")
dbListTables(con)
dbListFields(con, "RUNS")
run_data = dbGetQuery(con, "Select method_id, run_id, solution, run_time, start_time, stop_time from RUNS")
length(run_data)

run_data$method_id = as.factor(run_data$method_id)
str(run_data)
aov_run_data = aov(run_time ~ method_id, run_data)
sm = summary(aov_run_data);sm

pdf("result/plots_py_gurobi_r.pdf")
par(mfrow=c(2,2)) 
plt0 = plot(run_time ~ method_id,run_data)

#type "b" => show points and lines
plt1 = plot(run_data$run_id[run_data$method_id=="1"], run_data$run_time[run_data$method_id=="1"], type="b",xlim=range(run_data$run_id), ylim=range(run_data$run_time))
lines(run_data$run_id[run_data$method_id=="2"], run_data$run_time[run_data$method_id=="2"], col=2, type="b")
lines(run_data$run_id[run_data$method_id=="3"], run_data$run_time[run_data$method_id=="3"], col=3, type="b")

plt2 = qqnorm(aov_run_data$resid)
plt3 = qqline(aov_run_data$resid)
plt4 = plot(aov_run_data$fitted,aov_run_data$resid)
plt5 = abline(h=0)  #Add the horizontal axis
dev.off()







windows()
par(mfrow=c(2,2)) 
plt0 = plot(run_time ~ method_id,run_data)

#type "b" => show points and lines
plt1 = plot(run_data$run_id[run_data$method_id=="1"], run_data$run_time[run_data$method_id=="1"], type="b",xlim=range(run_data$run_id), ylim=range(run_data$run_time))
lines(run_data$run_id[run_data$method_id=="2"], run_data$run_time[run_data$method_id=="2"], col=2, type="b")
lines(run_data$run_id[run_data$method_id=="3"], run_data$run_time[run_data$method_id=="3"], col=3, type="b")



plt2 = qqnorm(aov_run_data$resid)
plt3 = qqline(aov_run_data$resid)
plt4 = plot(aov_run_data$fitted,aov_run_data$resid)
plt5 = abline(h=0)  #Add the horizontal axis

Sys.sleep(5)

dev.off()

print('R Scripts Succeeded')

